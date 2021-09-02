#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Test balance sheet statement"""

import unittest
import sys
from src.balance_sheet import Reporter

class MinimalLedger(unittest.TestCase):
    """Test Minimal ledger"""
    def test_default_greeting_set(self):
        """Test documentation goes here."""
        reporter = Reporter(year=2021, month=8, file='tests/resources/minimal/main.bean')
        report = reporter.generate()
        self.assertGreater(len(report), 0)

if __name__ == '__main__':
    unittest.main()
