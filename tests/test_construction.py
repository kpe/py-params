# coding=utf-8
#
# created by kpe on 15.03.2019 at 11:03 PM
#

from __future__ import division, absolute_import, print_function

import unittest

from params import Params


class MyParams(Params):
    param_a = True
    param_b = 1


class ParamsConstructionTest(unittest.TestCase):
    def test_defaults(self):
        expected = {'param_a': True, 'param_b': 1}
        self.assertEqual(expected, MyParams.defaults())

        params = MyParams()
        self.assertEqual(expected, dict(params))
        self.assertEqual(params.param_a, True)
        self.assertEqual(params.param_b, 1)

        params = MyParams(param_a=False, param_b=3)
        expected = {'param_a': False, 'param_b': 3}
        self.assertEqual(expected, dict(params))
        self.assertEqual(params.param_a, False)
        self.assertEqual(params.param_b, 3)
        self.assertEqual(params['param_a'], False)
        self.assertEqual(params['param_b'], 3)

        params = MyParams()
        params.param_a = False
        params.param_b = 4
        expected = {'param_a': False, 'param_b': 4}
        self.assertEqual(expected, params)
        self.assertEqual(params.param_a, False)
        self.assertEqual(params.param_b, 4)
        self.assertEqual(params['param_a'], False)
        self.assertEqual(params['param_b'], 4)

        params['param_a'] = True
        params['param_b'] = 5
        self.assertEqual(params.param_a, True)
        self.assertEqual(params.param_b, 5)

        try:
            params.param_c = 3
            self.fail()
        except AttributeError:
            pass
        try:
            params['param_c'] = 3
            self.fail()
        except AttributeError:
            pass


if __name__ == '__main__':
    unittest.main()
