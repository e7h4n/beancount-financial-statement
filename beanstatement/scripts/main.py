#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=no-value-for-parameter
"""命令行执行器"""
import click
from beanstatement.balance_sheet import Reporter

__version__ = '0.8.2'


@click.command()
@click.option('--year', help='Year.', type=click.INT, required=True)
@click.option('--month', help='Month.', type=click.INT, required=True)
@click.option('--beancount', help='Beancount ledger file.',
              type=click.Path(exists=True), required=True)
@click.version_option(__version__)
def main(year, month, beancount):
    """命令行执行器."""

    reporter = Reporter(year, month, beancount)
    print(reporter.generate())


if __name__ == '__main__':
    main()
