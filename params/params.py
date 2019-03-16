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

    def __init__(self, **kwargs):
        super(Params, self).__init__()
        self.update(self.__class__.defaults())
        self.update(kwargs)

    def __getattribute__(self, attr):
        if attr != 'defaults' and attr in self.defaults():
            return self.__getitem__(attr)
        return object.__getattribute__(self, attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        if key not in self.defaults():
            raise AttributeError("Setting unexpected parameter '{}' "
                                 "in Params instance '{}'".format(key, self.__class__.__name__))
        super(Params, self).__setitem__(key, value)

    @classmethod
    def defaults(cls):
        """ Aggregate all class fields in the class hierarchy to a dict. """

        if '_defaults' in cls.__dict__:
            return cls.__dict__['_defaults']

        result = {}
        for base in cls.__bases__:
            if issubclass(base, Params):
                result.update(base.defaults())

        result.update(dict(filter(lambda t: (not t[0].startswith('_') and
                                             not callable(getattr(cls, t[0]))),
                                  cls.__dict__.items())))

        cls._defaults = result
        return cls._defaults

    @classmethod
    def from_dict(cls, params):
        """ Constructs from dict and returns unused dict items. """

        if not params:
            return cls(), {}   # use default constructor

        # extract unused args
        keys = cls.defaults().keys()
        cls_args, rest_args = zip(*list(map(lambda p: (p, None) if p[0] in keys else (None, p),
                                            params.items())))

        def is_not_none(x):
            return x is not None

        cls_args  = dict(filter(is_not_none, cls_args))
        rest_args = dict(filter(is_not_none, rest_args))

        instance = cls(**dict(cls_args))
        return instance, rest_args

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
