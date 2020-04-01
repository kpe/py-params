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
        self.assertEqual(expected, dict(MyParams()))

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

    def test_from_dict(self):
        params_dict = {'param_a': 3,
                       'param_b': 4,
                       'param_c': 5}
        params, other = MyParams.from_dict(params_dict)
        self.assertEqual({'param_a': 3, 'param_b': 4}, params)
        self.assertEqual({'param_c': 5}, other)
        self.assertIsInstance(params, MyParams)
        self.assertIsInstance(other, dict)

        params = MyParams.from_dict(params_dict, return_unused=False)
        self.assertEqual({'param_a': 3, 'param_b': 4}, params)
        self.assertIsInstance(params, MyParams)

        params = MyParams.from_dict(params_dict, return_unused=False, return_instance=False)
        self.assertEqual({'param_a': 3, 'param_b': 4}, params)
        self.assertIsInstance(params, dict)

    def test_construct_dict(self):
        params = MyParams(param_a=99)
        self.assertEqual(99, params.param_a)
        params = MyParams(params, param_b=101)
        self.assertEqual(99, params.param_a)
        self.assertEqual(101, params.param_b)
        params = MyParams(params, param_a=101)
        self.assertEqual(101, params.param_a)
        self.assertEqual(101, params.param_b)

    def test_field_mutability(self):
        params = MyParams(param_a=1)
        try:
            params = MyParams(param_c=3)
            self.fail("Setting param_c should not be possible")
        except AttributeError:
            pass

        try:
            params.update(param_c=3)
            self.fail("Setting param_c should not be possible")
        except AttributeError:
            pass
        params.update({"param_a": 3})
        params.update([("param_a", 4)])


if __name__ == '__main__':
    unittest.main()
