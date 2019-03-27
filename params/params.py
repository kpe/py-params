# coding=utf-8
#
# created by kpe on 16.03.2019 at 12:56 AM
#

from __future__ import division, absolute_import, print_function

import json


class Params(dict):
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
    def from_json_string(cls, json_string):
        """ Deserializes this instance from a JSON string."""
        return cls(**json.loads(json_string))

    '''
    @classmethod
    def from_json_file(cls, json_file):
        """Constructs a `BertConfig` from a json file of parameters."""
        with tf.gfile.GFile(json_file, "r") as reader:
            text = reader.read()
        return cls(**json.loads(text))
    '''
