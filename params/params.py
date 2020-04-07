# coding=utf-8
#
# created by kpe on 16.03.2019 at 12:56 AM
#

from __future__ import division, absolute_import, print_function

import json
import inspect
from typing import Text, Type, Any, Dict

import argparse


class Param:
    """ Provides a parameter specification to be used within a Params instance. """
    def __init__(self, value, doc: Text = None, dtype: Type = None, required: bool = False, params_class=None):
        """
        Constructs a parameter specification to be used in a Params instance:

        Example:

            import params ass pp

            class MyParams(pp.Params):
                some_parameter    = pp.Param(0.9, doc="some description for the some_parameter parameter")
                another_parameter = 1

        :param value: default value for the parameter
        :param doc: (Optional) document string
        :param dtype: (Optional) type
        :param required:  default is True.
        """
        self.params_class = params_class
        self._default_value = value
        self.doc_string = doc
        self.required = required
        self.dtype = dtype
        if dtype is None and value is not None and not callable(value):
            self.dtype = type(value)
        if value is not None and not callable(value):
            if not isinstance(value, self.dtype):
                raise RuntimeError(f"Param({value}) does not match dtype:[{self.dtype}]")
        self.name = None
        self.is_property = callable(value)

    @property
    def default_value(self):
        return self._default_value(self.params_class) if self.is_property else self._default_value

    def value(self, params):
        return self._default_value(params) if self.is_property else getattr(self.name, params)


class Params(dict):
    """ Base class for defining safe parameter dictionaries.

    Example:
       Use by defining default parameter values as class variables,
       and then use or update the instance variables like this::

            import params as pp

            class MyParams(pp.Params):
                my_param = 1.0               # defaults to 1.0

            params = MyParams(my_param=2.0)           # override defaults
            params.my_param = 3.0                     # member set/get
            params['my_param'] = 3.0                  # access as dict
            assert dict(params) == {'my_param': 3.0}  # access as dict

            params.another_param = 4.0            # raises ValueError
            params = MyParams(another_param=2.0)  # raises ValueError
    """

    __specs    : Dict[Text, Param] = {}
    __defaults : Dict[Text, Any]   = {}

    def __init_subclass__(cls, **kwargs):
        """ Aggregates the Param spec of the parameters over the hierarchy. """
        base_specs = {}
        for base in cls.__bases__:
            if issubclass(base, Params):
                base_specs.update(base.__specs)

        cls_specs = []  # evaluate in order of declaration
        for attr, value in cls.__dict__.items():
            if attr.startswith("_") or callable(getattr(cls, attr)):
                continue

            attr_val = getattr(cls, attr)
            if isinstance(attr_val, property):
                param_spec = Param(attr_val.fget, params_class=cls)
            elif not isinstance(attr_val, Param):
                param_spec = Param(value)
            else:
                param_spec = attr_val

            param_spec.name = attr
            cls_specs.append((attr, param_spec))

        _specs = {}
        for attr, value in list(base_specs.items()) + cls_specs:
            setattr(cls, attr, value.default_value)
            _specs[attr] = value

        cls.__specs = _specs
        cls.__defaults = {key: val.default_value for key, val in cls.__specs.items()}

    def __init__(self, *args, **kwargs):
        super(Params, self).__init__()
        self.update(self.__defaults)   # start with default values
        self.update(dict(*args))       # override with tuple list
        self.update(kwargs)            # override with kwargs
        # update any overridden @property parameters
        prop_specs = list(filter(lambda spec: spec.is_property,
                                 self.__class__.__specs.values()))

        for spec in prop_specs:
            self.update({spec.name: spec.value(self)})

    def update(self, arg=None, **kwargs):   # see dict.update()
        if arg:
            keys = getattr(arg, "keys") if hasattr(arg, "keys") else None
            if keys and (inspect.ismethod(keys) or inspect.isbuiltin(keys)):
                for key in arg:
                    self[key] = arg[key]
            else:
                for key, v in arg:
                    self[key] = v
        for key in kwargs:
            self[key] = kwargs[key]

    def __getattribute__(self, attr):
        if not attr.startswith("_") and attr in self.__defaults:
            if self.__specs[attr].is_property:
                return self.__specs[attr].value(self)
            else:
                return self.__getitem__(attr)
        return object.__getattribute__(self, attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        if key not in self.__defaults:
            raise AttributeError("Setting unexpected parameter '{}' "
                                 "in Params instance '{}'".format(key, self.__class__.__name__))
        super(Params, self).__setitem__(key, value)

    @classmethod
    def from_dict(cls, args, return_instance=True, return_unused=True):
        """ Constructs from given ``args`` dict and returns the unused ``args``.

        :param args: keyword dictionary with parameters
        :param return_instance: False to return a dictionary instead of a Params instance.
               **N.B.** the `dict` returned by `MyParams.from_dict(return_instance=False))`
               does not include the `MyParams` default params (unlike an instance
               created with `return_instance=True`).
        :param return_unused: True to return the arguments not valid for the current class.
        :return: a tuple (params, other) of params and a dict of unused arguments,
                 where params is either a dict or a Params instance (where ``return_instance=True``).
        """

        def is_not_none(x):
            return x is not None

        cls_args, unused_args = {}, {}
        if args:
            # extract unused args
            keys = cls.__defaults.keys()
            cls_args, unused_args = zip(*list(map(lambda p: (p, None) if p[0] in keys else (None, p),
                                                  args.items())))

            cls_args    = dict(filter(is_not_none, cls_args))
            unused_args = dict(filter(is_not_none, unused_args))

        params = cls(**cls_args) if return_instance else cls_args

        if return_unused:
            return params, unused_args
        return params

    #
    # serialization
    #

    def to_json_string(self):
        """ Serializes this instance to a JSON string."""
        return json.dumps(dict(self), indent=2, sort_keys=True) + "\n"

    @classmethod
    def from_json_string(cls, json_string: Text, check_params=False):
        """ Deserializes this instance from a JSON string.
        :param json_string: a JSON string to parse
        :param check_params: whether to throw an exception when
               json_string contains params not compatible with the current instance.
        """
        if check_params:
            return cls(**json.loads(json_string))
        else:
            return cls.from_dict(json.loads(json_string), return_instance=True, return_unused=False)

    @classmethod
    def from_json_file(cls, json_file, check_params=False):
        """Constructs an instance from a json file."""
        try:
            import tensorflow as tf
            open_file = tf.io.gfile.GFile  # pragma: no cover
        except Exception:                  # pragma: no cover
            open_file = open

        try:
            with open_file(json_file, "r") as reader:
                text = reader.read()
            return cls.from_json_string(text, check_params=check_params)
        except Exception as err:
            print("Failed to read {} instance from: {}".format(cls.__name__, json_file), err)
            return None

    def to_json_file(self, file_path, **kwargs):
        """Writes the instance to a json file."""
        try:
            import tensorflow as tf
            open_file = tf.io.gfile.GFile  # pragma: no cover
        except Exception:                  # pragma: no cover
            open_file = open

        try:
            with open_file(file_path, "w") as fp:
                json.dump(self, fp, **kwargs)
            return file_path
        except Exception as err:
            print("Failed to write {} instance to: {}".format(self.__class__.__name__, file_path), err)
            return None

    def clone(self, **kwargs):
        """
        Creates a clone.
        :param kwargs: parameters to override in the clone.
        """
        args = dict(self)
        args.update(**kwargs)
        return self.__class__(**args)

    @classmethod
    def to_argument_parser(cls) -> argparse.ArgumentParser:
        def arg_name(param_name: Text):
            result = param_name.lower().replace("_", "-")
            return result

        parser = argparse.ArgumentParser()
        for attr, spec in cls.__specs.items():
            if spec.doc_string is None:
                continue
            name = arg_name(spec.name)
            add_argument_args = {
                "type": spec.dtype,
                "required": spec.required,
                "help": spec.doc_string,
                "default": spec.default_value
            }
            if spec.dtype == bool:
                add_argument_args.update({
                    "type": _str2bool, "nargs": "?", "const": True
                })
            parser.add_argument("--{}".format(name), **add_argument_args)
        return parser


def _str2bool(v: Text) -> bool:
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')
