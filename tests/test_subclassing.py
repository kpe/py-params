# coding=utf-8
#
# created by kpe on 16.03.2019 at 1:22 AM
#

from __future__ import division, absolute_import, print_function

import unittest

import params as pp


class BaseParams(pp.Params):
    param_a = "a"
    param_b = "b"


class SubParams(BaseParams):
    param_a = "Sa"
    param_c = "Sc"


class SubParamsA(SubParams):
    param_d = "aD"
    param_e = "aE"


class SubParamsB(SubParams):
    param_f = 'SBf'

    @property
    def param_g(self):
        return "SBBg_" + self.param_b

    @property
    def param_a(self):
        return "SBBa_" + self.param_g + self.param_c


class MySubParams(SubParamsA, SubParamsB):
    param_h = "MSh"
    param_j = "MSj"

    @property
    def param_c(self):
        return "MSc_" + self.param_g


class AnotherSubParams(MySubParams):
    @property
    def param_h(self):
        return "ASh_" + self.param_d

    @property
    def param_g(self):
        return "ASg_" + self.param_h



class ParamsSubclassingTest(unittest.TestCase):
    def test_subclassing(self):
        params = SubParams()
        expected = {"param_a": "Sa", "param_b": "b", "param_c": "Sc"}
        self.assertEqual(dict(params), expected)

        params = SubParams(param_b="bb")
        params.param_c = "cc"
        params.param_a = "aa"
        expected = {"param_a": "aa", "param_b": "bb", "param_c": "cc"}
        self.assertEqual(dict(params), expected)

        params = BaseParams()
        try:
            params.param_c = "cc"
            self.fail()
        except AttributeError:
            pass

        params = SubParams(param_b="bb").clone(param_c="cc")
        expected = {"param_b": "bb", "param_a": "Sa", "param_c": "cc"}
        self.assertEqual(dict(params), expected)

    def test_hierarchy(self):
        params = MySubParams(param_f="SBf")
        self.assertEqual(params.param_b, "b")
        self.assertEqual(params.param_a, "SBBa_SBBg_bMSc_SBBg_b")

        MySubParams.to_argument_parser().print_help()

        self.assertEqual(params.param_f, "SBf")
        self.assertEqual(MySubParams.param_f, "SBf")

    def test_hierarchy_override(self):
        params = AnotherSubParams(param_d='Z')
        self.assertEqual(params.param_g, "ASg_ASh_Z")


if __name__ == '__main__':
    unittest.main()
