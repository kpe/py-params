# coding=utf-8
#
# created by kpe on 16.03.2019 at 1:22 AM
#

from __future__ import division, absolute_import, print_function

import unittest

from params import Params


class BaseParams(Params):
    param_a = True
    param_b = 1


class SubParams(BaseParams):
    param_c = 'a'
    param_a = False

class SubParamsA(SubParams):
    param_d = 'A'
    param_e = False

class SubParamsB(SubParams):
    param_f = 'B'
    param_g = False

class MySubParams(SubParamsA, SubParamsB):
    param_h = 'a'
    param_j = False




class ParamsSubclassingTest(unittest.TestCase):
    def test_subclassing(self):
        Params()
        params = SubParams()
        expected = {'param_a': False, 'param_b': 1, 'param_c': 'a'}
        self.assertEqual(dict(params), expected)

        params = SubParams(param_b=2)
        params.param_c = 'b'
        params.param_a = True
        expected = {'param_a': True, 'param_b': 2, 'param_c': 'b'}
        self.assertEqual(dict(params), expected)

        params = BaseParams()
        try:
            params.param_c = 'c'
            self.fail()
        except AttributeError:
            pass

        params = SubParams(param_b=2).clone(param_c=3)
        expected = {'param_b': 2, 'param_a': False, 'param_c': 3}
        self.assertEqual(dict(params), expected)

    def test_hierarchy(self):
        params = MySubParams()
        self.assertEqual(params.param_b, 1)
        self.assertEqual(params.param_a, False)
        MySubParams.to_argument_parser().print_help()

if __name__ == '__main__':
    unittest.main()
