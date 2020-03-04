# coding=utf-8
#
# created by kpe on 16.03.2019 at 12:56 AM
#

from __future__ import division, absolute_import, print_function

import json
import types
import inspect


class Params(dict):  # TODO use collections.UserDict instead of dict - see #1
    """ Base class for defining safe parameter dictionaries.

    Example:
       Use by defining default parameter values as class variables,
       and then use or update the instance variables like this::

            class MyParams(Params):
                my_param = 1.0               # defaults to 1.0

            params = MyParams(my_param=2.0)           # override defaults
            params.my_param = 3.0                     # member set/get
            params['my_param'] = 3.0                  # access as dict
            assert dict(params) == {'my_param': 3.0}  # access as dict

            params.another_param = 4.0            # raises ValueError
            params = MyParams(another_param=2.0)  # raises ValueError
    """

    def __init__(self, *args, **kwargs):
        super(Params, self).__init__()
        self.update(self.__defaults())
        self.update(dict(*args))
        self.update(kwargs)

    def update(self, arg=None, **kwargs):
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
        if not attr.startswith("_") and attr in self.__defaults():
            return self.__getitem__(attr)
        return object.__getattribute__(self, attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        if key not in self.__defaults():
            raise AttributeError("Setting unexpected parameter '{}' "
                                 "in Params instance '{}'".format(key, self.__class__.__name__))
        super(Params, self).__setitem__(key, value)

    @classmethod
    def __defaults(cls):
        """ Aggregate all class fields in the class hierarchy to a dict. """

        if '_defaults' in cls.__dict__:
            return cls._defaults

        result = {}
        for base in cls.__bases__:
            if issubclass(base, Params):
                result.update(base.__defaults())

        for attr, value in cls.__dict__.items():
            if attr.startswith("_") or callable(getattr(cls, attr)):
                continue
            result[attr] = value

        cls._defaults = result
        return cls._defaults

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
            keys = cls.__defaults().keys()
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
    def from_json_string(cls, json_string, check_params=False):
        """ Deserializes this instance from a JSON string.
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
            print("Failed to read {} instance from: {}".format(cls.__name__, json_file))
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
            print("Failed to write {} instance to: {}".format(self.__class__.__name__, file_path))
            return None

    def clone(self, **kwargs):
        """
        Creates a clone.
        :param kwargs: parameters to override in the clone.
        """
        args = dict(self)
        args.update(**kwargs)
        return self.__class__(**args)
