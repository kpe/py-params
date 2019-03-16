# coding=utf-8
#
# created by kpe on 16.03.2019 at 2:56 AM
#

from __future__ import division, absolute_import, print_function

import unittest

from params import Params


class SomeParams(Params):
    param_a = 1


class ParamsSerializationTest(unittest.TestCase):
    def test_serialization(self):
        params, rest = SomeParams.from_dict({'param_a': 2})
        self.assertEqual(dict(params), {'param_a': 2})
        self.assertEqual(rest, {})

        params, rest = SomeParams.from_dict({'param_a': 5, 'unused': 3})
        self.assertEqual(dict(params), {'param_a': 5})
        self.assertEqual(rest, {'unused': 3})

        params, rest = SomeParams.from_dict({})
        self.assertEqual(dict(params), {'param_a': 1})
        self.assertEqual(rest, {})

    def test_json(self):
        params = SomeParams.from_json_string(SomeParams().to_json_string())
        self.assertEqual(params, {'param_a': 1})


if __name__ == '__main__':
    unittest.main()
