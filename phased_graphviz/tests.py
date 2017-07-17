from unittest import TestCase

from .util import parse_phases


class PhasedGraphvizTestCase(TestCase):
    def test_phases(self):
        self.assertEqual({1, 2}, parse_phases("1-", 1, 2))
        self.assertEqual({1, 2, 3, 4}, parse_phases("1-4", 1, 2))
        self.assertEqual({1, 2, 3, 4}, parse_phases("-4", 1, 2))
        self.assertEqual({0, 1}, parse_phases("-1", 0, 2))
        self.assertEqual({2}, parse_phases("2-", 0, 0))
        self.assertEqual({1, 3}, parse_phases("1,3-", 0, 0))
        self.assertEqual({1, 3, 4}, parse_phases("1,3-", 0, 4))
