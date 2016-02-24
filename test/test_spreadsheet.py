import os
import sys
import unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pyopendoc.spreadsheet import OpenSpreadsheetDocument

class TestAddressToColumnsRows(unittest.TestCase):

    def setUp(self):
        self.ods = OpenSpreadsheetDocument()

    def test_colrow_from_address_default(self):
        column, row = self.ods._get_colrow_from_address() # "A1"
        self.assertEqual(column, 0)
        self.assertEqual(row, 0)

    def test_colrow_from_address_normal_small(self):
        column, row = self.ods._get_colrow_from_address("C4")
        self.assertEqual(column, 2)
        self.assertEqual(row, 3)

        column, row = self.ods._get_colrow_from_address("F18")
        self.assertEqual(column, 5)
        self.assertEqual(row, 17)

        column, row = self.ods._get_colrow_from_address("M67")
        self.assertEqual(column, 12)
        self.assertEqual(row, 66)

    def test_colrow_from_address_normal_big(self):
        column, row = self.ods._get_colrow_from_address("AB12")
        self.assertEqual(column, 27)
        self.assertEqual(row, 11)

    def test_colrow_from_address_extreme_big(self):
        column, row = self.ods._get_colrow_from_address("ZZ100")
        self.assertEqual(column, 701)
        self.assertEqual(row, 99)

    def test_colrow_from_address_extreme_bigger(self):
        column, row = self.ods._get_colrow_from_address("AAA101")
        self.assertEqual(column, 702)
        self.assertEqual(row, 100)

        column, row = self.ods._get_colrow_from_address("AAK256")
        self.assertEqual(column, 712)
        self.assertEqual(row, 255)

        column, row = self.ods._get_colrow_from_address("AAA101")
        self.assertEqual(column, 702)
        self.assertEqual(row, 100)

    def test_colrow_from_colrow_max_col(self):
        column, row = self.ods._get_colrow_from_address("AMJ2071")
        self.assertEqual(column, 1023)
        self.assertEqual(row, 2070)


class TestColumnsRowsToAddresses(unittest.TestCase):

    def setUp(self):
        self.ods = OpenSpreadsheetDocument()

    def test_address_from_colrow_default(self):
        address = self.ods._get_address_from_colrow() # 0, 0
        self.assertEqual(address, "A1")

    def test_address_from_colrow_normal_small(self):
        address = self.ods._get_address_from_colrow(2, 3)
        self.assertEqual(address, "C4")

    def test_address_from_colrow_normal_big(self):
        address = self.ods._get_address_from_colrow(27, 11)
        self.assertEqual(address, "AB12")

    def test_address_from_colrow_extreme_big(self):
        address = self.ods._get_address_from_colrow(701, 99)
        self.assertEqual(address, "ZZ100")

    def test_address_from_colrow_extreme_bigger(self):
        address = self.ods._get_address_from_colrow(702, 100)
        self.assertEqual(address, "AAA101")


if __name__ == "__main__":
    unittest.main()

