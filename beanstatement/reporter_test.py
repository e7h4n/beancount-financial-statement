#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Test balance sheet statement"""

import unittest
from bs4 import BeautifulSoup
from beanstatement.reporter import Reporter


class MinimalLedger(unittest.TestCase):
    """Test Minimal ledger"""

    def test_default_greeting_set(self):
        """Test documentation goes here."""
        reporter = Reporter(year=2021, month=8,
                            file='beanstatement/test_resources/minimal/main.bean')
        report = reporter.generate()

        soup = BeautifulSoup(report, 'html.parser')
        total_equity = soup.select('tr.level-0.total')[-1].select('td')[-1].text
        self.assertEqual(total_equity, '12,345,678.00')

    def test_working_currency_title(self):
        """Test documentation goes here."""
        reporter = Reporter(year=2021, month=8,
                            file='beanstatement/test_resources/minimal/main.bean')
        report = reporter.generate()

        soup = BeautifulSoup(report, 'html.parser')
        title = soup.select('#table-title')[0].text
        self.assertEqual(title, 'As of (USD)')


if __name__ == '__main__':
    unittest.main()
