# coding=utf-8
#
# created by kpe on 03.04.2020 at 6:08 PM
#

from __future__ import division, absolute_import, print_function

import unittest

import params as pp


class BaseClass:
    def __init__(self, base_arg, base_kwarg=None):
        self.base_arg   = base_arg
        self.base_kwarg = base_kwarg


class SubClass(pp.WithParams, BaseClass):
    class Params(pp.WithParams.Params):
        sub_param = "test"

    def _construct(self, sub_arg, *args, **kwargs):
        super()._construct(*args, **kwargs)
        self.sub_arg = sub_arg


class SubSubClass(SubClass):
    class Params(SubClass.Params):
        sub_sub_param = "test"

    def _construct(self, sub_sub_arg, *args, **kwargs):
        super()._construct(*args, **kwargs)
        self.sub_sub_arg = sub_sub_arg


class WithParamsTest(unittest.TestCase):

    def check_instance(self, wp):
        if isinstance(wp, SubSubClass):
            self.assertEqual(wp.sub_sub_arg, "sub_sub_arg")
            self.assertEqual(wp.params.sub_sub_param, "sub_sub_param")
        if isinstance(wp, SubClass):
            self.assertEqual(wp.sub_arg, "sub_arg")
            self.assertEqual(wp.params.sub_param, "sub_param")
        if isinstance(wp, BaseClass):
            self.assertEqual(wp.base_arg, "base_arg")
            self.assertEqual(wp.base_kwarg, "base_kwarg")

        self.assertEqual(wp.sub_arg, "sub_arg")
        self.assertEqual(wp.base_kwarg, "base_kwarg")
        self.assertEqual(wp.params.sub_param, "sub_param")

    def test_with_params(self):
        wp = SubClass("sub_arg", "base_arg", base_kwarg="base_kwarg", sub_param="sub_param")
        self.check_instance(wp)

        wp = SubSubClass("sub_sub_arg", "sub_arg", "base_arg", base_kwarg="base_kwarg",
                         sub_param="sub_param", sub_sub_param="sub_sub_param")
        self.check_instance(wp)

    def test_from_params(self):
        params = SubSubClass.Params()
        wp = SubSubClass.from_params(params, "sub_sub_arg", "sub_arg", "base_arg",
                                     sub_param="sub_param", base_kwarg="base_kwarg",
                                     sub_sub_param="overridden")
        self.assertEqual(wp.params.sub_sub_param, "overridden")
        wp.params.sub_sub_param = "sub_sub_param"
        self.check_instance(wp)

    def test_param_create(self):
        wp = SubSubClass.Params().create(
            "sub_sub_arg", "sub_arg", "base_arg",
            sub_param="sub_param", base_kwarg="base_kwarg", sub_sub_param="sub_sub_param")
        self.check_instance(wp)

