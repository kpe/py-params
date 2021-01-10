# coding=utf-8
#
# created by kpe on 31.03.2020 at 12:45 PM
#

from __future__ import division, absolute_import, print_function

import unittest

import params as pp


class MyParams(pp.Params):
    number_of_things   = pp.Param(1, doc="Specifies the number of things", required=True)
    use_other_things   = pp.Param(True, doc="Whether to use other things")
    additional_info    = pp.Param(None, doc="Any additional info", dtype=str)
    hidden_param       = 4  # not accessible on the CLI
    float_param        = pp.Param(None, dtype=float, doc="A float parameter")

    _non_parameter     = 1  # all _* class fields would be hidden

    @property
    def param_z(self):                          # a derived parameter
        return self._non_parameter + 1

    def get_something_else(self, value: int):   # a derived callable
        return self.number_of_things + value


class MyParamsWithCommand(MyParams):
    cmd = pp.Param(None, doc="Command to execute", positional=True)


class ParamsDecorationTest(unittest.TestCase):

    def test_decoration(self):
        params = MyParams()
        self.assertEqual(params.number_of_things, 1)
        self.assertEqual(params.use_other_things, True)
        self.assertEqual(params.additional_info, None)
        self.assertEqual(params.param_z, 2)
        self.assertEqual(params.get_something_else(3), 4)

    def test_argument_parser(self):
        parser = MyParams.to_argument_parser()
        parser.print_help()

        def error_fn(msg, *args, **kwargs):
            raise Exception(msg)
        parser.error = error_fn  # supress sys.exit

        args = parser.parse_args(["--use-other-things", False, "--number-of-things", "7"])
        self.assertEqual(args.use_other_things, False)

        args = parser.parse_args(["--use-other-things", "1", "--float-param", "1e-4", "--number-of-things", "8"])
        self.assertEqual(args.use_other_things, True)
        self.assertEqual(args.float_param, 1e-4)

        try:
            args = parser.parse_args(["--use-other-things", "f"])
            self.fail("ArgumentError expected - required param missing")
        except Exception:
            pass

        try:
            class AParams(pp.Params):
                parm = pp.Param(2, dtype=bool)
            self.fail("RuntimeError expected - type mismatch")
        except Exception:
            pass

        try:
            args = parser.parse_args(["--use-other-things", "1e-6", "--number-of-things", "3"])
            self.fail("ArgumentTypeError expected")
        except Exception:
            pass

    def test_arg_parser_with_command(self):
        parser = MyParamsWithCommand.to_argument_parser()
        parser.print_help()

        def error_fn(msg, *args, **kwargs):
            raise Exception(msg)
        parser.error = error_fn  # supress sys.exit

        args = parser.parse_args(["start", "--use-other-things", False, "--number-of-things", "7"])
        self.assertEqual(args.use_other_things, False)
        inst = MyParamsWithCommand(args._get_kwargs())
        self.assertEqual(inst.cmd, 'start')

        args = parser.parse_args(["--use-other-things", False, "--number-of-things", "7", "stop"])
        self.assertEqual(args.use_other_things, False)
        inst = MyParamsWithCommand(args._get_kwargs())
        self.assertEqual(inst.cmd, 'stop')

