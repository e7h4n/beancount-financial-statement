#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Test balance sheet statement"""

import unittest
import sys
from src.balance_sheet import Reporter
from bs4 import BeautifulSoup

class MinimalLedger(unittest.TestCase):
    """Test Minimal ledger"""
    def test_default_greeting_set(self):
        """Test documentation goes here."""
        reporter = Reporter(year=2021, month=8, file='tests/resources/minimal/main.bean')
        report = reporter.generate()

        soup = BeautifulSoup(report, 'html.parser')
        total_equity = soup.select('tr.level-0.total')[-1].select('td')[-1].text
        self.assertEqual(total_equity, '12,345,678.00')

if __name__ == '__main__':
    unittest.main()
