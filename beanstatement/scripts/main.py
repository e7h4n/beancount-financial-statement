#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=no-value-for-parameter
"""命令行执行器"""
import click
from beanstatement import __version__
from beanstatement.reporter import Reporter


@click.command(no_args_is_help=True)
@click.option('--year', help='Year.', type=click.INT, required=True)
@click.option('--month', help='Month.', type=click.INT, required=True)
@click.option('--beancount', help='Beancount ledger file.',
              type=click.Path(exists=True), required=True)
@click.version_option(__version__)
def main(year, month, beancount):
    """Beancount financial statement tool"""

    reporter = Reporter(year, month, beancount)
    print(reporter.generate())


if __name__ == '__main__':
    main()
