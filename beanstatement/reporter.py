#!/usr/bin/env python
# pylint: disable=isinstance-second-argument-not-valid-type
"""资产报告生成器"""
import calendar
import datetime
import importlib.resources as pkg_resources
import os
from datetime import timedelta
from decimal import Decimal

import pystache
from beancount.core.convert import convert_amount
from beancount.core.data import Custom
from beancount.core.data import Open
from beancount.core.getters import get_account_open_close
from beancount.core.number import D
from beancount.core.prices import build_price_map
from beancount.loader import load_file
from beancount.query import query

from . import templates


def parse_report_layout(layout_file):
    """分析布局文件，生成最终的完整布局"""

    with open(layout_file, encoding="utf-8") as f_p:
        layout_content = f_p.readlines()
    layout_content = [x.strip() for x in layout_content]

    report_layout = []
    unresolved = []
    for line in layout_content:
        last_section = None
        for section in line.split(":"):
            if last_section is None:
                last_section = section
            else:
                last_section = last_section + ":" + section

            same_context = len(unresolved) > 0 and unresolved[-1][
                "category"
            ].startswith(last_section)

            if same_context:
                continue

            first_unresolved = True
            while len(unresolved) > 0:
                last_unresolved_category = unresolved[-1]["category"]
                if last_section.startswith(last_unresolved_category):
                    break

                stack_top_section = unresolved.pop()
                if first_unresolved is True:
                    first_unresolved = False
                    stack_top_section["show_amount"] = True
                else:
                    report_layout.append(
                        {
                            "category": stack_top_section["category"],
                            "show_total": True,
                            "show_amount": True,
                        }
                    )

            report_layout.append(
                {
                    "category": last_section,
                    "show_amount": False,
                    "show_total": False,
                }
            )
            unresolved.append(report_layout[-1])

    first_unresolved = True
    while len(unresolved) > 0:
        stack_top_section = unresolved.pop()
        if first_unresolved is True:
            first_unresolved = False
            stack_top_section["show_amount"] = True
        else:
            report_layout.append(
                {
                    "category": stack_top_section["category"],
                    "show_total": True,
                    "show_amount": True,
                }
            )

    return report_layout


def add_months(sourcedate, months):
    """add month to an existed date"""

    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)


def sum_by_map(result_map, category, inventory):
    """sum inventory by category"""

    last_token = None
    for token in category.split(":"):
        if last_token is not None:
            last_token = last_token + ":" + token
        else:
            last_token = token

        if last_token not in result_map:
            result_map[last_token] = inventory
        else:
            result_map[last_token] = result_map[last_token] + inventory


def render(periods, sections, report_meta):
    """渲染模板"""

    template = pkg_resources.read_text(templates, "balance_sheet.mustache")

    return pystache.render(
        template,
        {
            "periods": periods,
            "sections": sections,
            "meta": report_meta,
        },
    )


class Reporter:
    """资产报告生成类"""

    entries = None
    option_map = None
    layout = None
    price_map = None
    year = None
    month = None
    working_currency = None

    def __init__(self, year, month, file, target="balance_sheet"):
        self.year = year
        self.month = month
        (entries, _, option_map) = load_file(file)
        self.entries = entries
        self.option_map = option_map

        layout = None
        for entry in entries:
            if isinstance(entry, Custom) is False:
                continue

            if entry.type != "finance-statement-option":
                continue

            if len(entry.values[0]) == 0:
                continue

            if (
                target == "balance_sheet"
                and entry.values[0].value == "balance_sheet_layout"
                and len(entry.values[0]) == 2
            ):
                layout = entry.values[1].value
            elif (
                target == "income_statement"
                and entry.values[0].value == "income_statement_layout"
                and len(entry.values[0]) == 2
            ):
                layout = entry.values[1].value
            elif (
                entry.values[0].value == "working_currency"
                and len(entry.values[0]) == 2
            ):
                self.working_currency = entry.values[1].value

        if layout is None:
            raise Exception(
                "Can't find balance_sheet_layout option, you should place a custom directive in the head of your ledger file"
            )

        layout = os.path.join(str(os.path.dirname(file)), layout)
        self.layout = parse_report_layout(layout)

        self.price_map = build_price_map(entries)

    def generate(self):
        """Generate Report"""

        (category_map, equity_map, category_accounts_map) = self.__parse_category()

        self.__check_layout(category_map, equity_map)

        (periods, reports) = self.__generate_report_data(category_map, equity_map)

        sections = self.__merge_data_and_layout(reports, category_accounts_map)

        return render(
            periods,
            sections,
            {
                "working_currency": self.working_currency,
            },
        )

    def unify_currency(self, inventory):
        """统一转换货币"""

        amount = D(0)
        for currency in inventory.currency_pairs():
            if currency[0] == self.working_currency:
                amount = amount + inventory.get_currency_units(currency[0]).number
            else:
                amount = (
                    amount
                    + convert_amount(
                        inventory.get_currency_units(currency[0]),
                        self.working_currency,
                        self.price_map,
                    ).number
                )

        ret = "{:,}".format(amount.copy_abs().quantize(Decimal(".01")))
        if amount < 0:
            ret = f"({ret})"

        return ret

    def __balance_report(self, year, month, category_map, equity_map):
        close_on = add_months(datetime.datetime(year, month, 1), 1)

        ret = query.run_query(
            self.entries,
            self.option_map,
            f"balances at cost from  CLOSE ON {str(close_on)} CLEAR",
        )

        account_balance_map = {}
        for balance in ret[1]:
            account = balance[0]
            inventory = balance[1]
            if account not in category_map:
                if account.startswith("Assets"):
                    raise Exception(
                        f'Assets account "{account}" doesn\'t have balance sheet field'
                    )

                if account.startswith("Liabilities"):
                    raise Exception(
                        'Liabilities account "{}" doesn\'t have balance sheet field'.format(
                            account
                        )
                    )
                continue

            sum_by_map(account_balance_map, category_map[account], inventory)
            sum_by_map(account_balance_map, equity_map[account], inventory)

        return account_balance_map

    def __parse_category(self):
        category_map = {}
        category_accounts_map = {}
        equity_map = {}
        accounts = get_account_open_close(self.entries)
        for name in accounts:
            directives = accounts[name]
            open_account = None
            for directive in directives:
                if isinstance(directive, Open):
                    open_account = directive
                    break

            if open_account is None:
                continue

            if "balance_sheet_category" not in open_account.meta:
                continue

            if "equity_category" not in open_account.meta:
                continue

            category = open_account.meta["balance_sheet_category"]
            category_map[open_account.account] = category

            equity_category = open_account.meta["equity_category"]
            equity_map[open_account.account] = equity_category

            if category not in category_accounts_map:
                category_accounts_map[category] = [open_account.account]
            else:
                category_accounts_map[category].append(open_account.account)

        return (category_map, equity_map, category_accounts_map)

    def __check_layout(self, category_map, equity_map):
        assert self.layout is not None

        dissociated_categories = set(category_map.values())
        dissociated_categories.update(equity_map.values())
        dissociated_categories = dissociated_categories.difference(
            [x["category"] for x in self.layout]
        )

        if len(dissociated_categories) > 0:
            dissociated_categories = sorted(dissociated_categories)
            raise Exception(
                'Some dissociated categories not included in balance sheet layout file: "{}"'.format(
                    '", "'.join(dissociated_categories)
                )
            )

    def __generate_report_data(self, category_map, equity_map):
        assert self.year is not None
        assert self.month is not None

        latest_month = datetime.datetime(self.year, self.month, 1)

        periods = []
        reports = []
        for i in range(12):
            report_date = add_months(latest_month, i - 11)
            report = self.__balance_report(
                report_date.year, report_date.month, category_map, equity_map
            )
            reports.append(report)

            periods.append(add_months(report_date, 1) + timedelta(days=-1))

        return (periods, reports)

    def __merge_data_and_layout(self, reports, category_accounts_map):
        assert self.layout is not None

        sections = []
        for line in self.layout:
            section = {
                "category": line["category"].split(":")[-1],
                "class": "level-" + str(line["category"].count(":")),
            }

            if line["category"] in category_accounts_map:
                section["accounts"] = "\n".join(
                    sorted(category_accounts_map[line["category"]])
                )

            if line["category"].count(":") == 0 and not line["show_total"]:
                section["category"] = line["category"].upper()

            if line["show_total"]:
                section["class"] = section["class"] + " total"
                section["category"] = "Total " + section["category"].lower()

            if line["show_amount"]:
                section["amounts"] = []
                for report in reports:
                    if line["category"] in report:
                        amount = report[line["category"]]
                        if line["category"].lower().find("liabilities") != -1:
                            amount = -amount
                        amount = self.unify_currency(amount)
                    else:
                        amount = "0.00"

                    section["amounts"].append(amount)

            sections.append(section)

        return sections
