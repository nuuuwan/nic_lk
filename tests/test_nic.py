import unittest
from unittest import TestCase

from nic_lk.core.NIC import NIC
from tests.examples import EXMPLE_LIST


class Test(TestCase):
    def test_version(self):
        for example in EXMPLE_LIST:
            nic = NIC(example['nic_no'])
            self.assertEqual(nic.to_dict(), example)


if __name__ == '__main__':
    unittest.main()
