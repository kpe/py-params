# coding=utf-8
#
# created by kpe on 16.03.2019 at 2:56 AM
#

from __future__ import division, absolute_import, print_function

import unittest
import tempfile

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

    def test_to_json_file(self):
        params = SomeParams.from_json_string(SomeParams().to_json_string())
        with tempfile.NamedTemporaryFile("w") as tf:
            tf.close()
            file_name = params.to_json_file(tf.name)
            self.assertIsNotNone(file_name)
            dparams = SomeParams.from_json_file(file_name)
            self.assertEqual(params, dparams)
            dparams = SomeParams.from_json_file(file_name, check_params=True)
            self.assertEqual(params, dparams)

    def test_to_json_file_fail(self):
        params = SomeParams.from_json_string(SomeParams().to_json_string())
        try:
            params.to_json_file("/proc/test")
            self.fail()
        except Exception:
            pass
        try:
            SomeParams.from_json_file("/proc/test")
            self.fail()
        except Exception:
            pass

    def test_yaml(self):
        params = SomeParams.from_yaml_string(SomeParams().to_yaml_string())
        self.assertEqual(params, {'param_a': 1})

    def test_to_yaml_file(self):
        params = SomeParams.from_yaml_string(SomeParams().to_yaml_string())
        with tempfile.NamedTemporaryFile("w") as tf:
            tf.close()
            file_name = params.to_yaml_file(tf.name)
            self.assertIsNotNone(file_name)
            dparams = SomeParams.from_yaml_file(file_name)
            self.assertEqual(params, dparams)
            dparams = SomeParams.from_yaml_file(file_name, check_params=True)
            self.assertEqual(params, dparams)

    def test_to_yaml_file_fail(self):
        params = SomeParams.from_yaml_string(SomeParams().to_yaml_string())
        try:
            params.to_yaml_file("/proc/test")
            self.fail()
        except Exception:
            pass
        try:
            SomeParams.from_yaml_file("/proc/test")
            self.fail()
        except Exception:
            pass

if __name__ == '__main__':
    unittest.main()
