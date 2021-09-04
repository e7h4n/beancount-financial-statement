#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=no-value-for-parameter
"""命令行执行器"""
import click
from src.balance_sheet import Reporter


@click.command()
@click.option('--year', help='Year.')
@click.option('--month', help='Month.')
@click.option('--beancount', help='Beancount ledger file.')
def main(year, month, beancount):
    """命令行执行器."""

    reporter = Reporter(int(year), int(month), beancount)
    print(reporter.generate())


if __name__ == '__main__':
    main()
