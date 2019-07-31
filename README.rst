
Params
======

|Build Status| |Coverage Status| |Version Status| |Python Versions| |Downloads|

A type safe dictionary class in python.


LICENSE
-------

MIT. See `License File <https://github.com/kpe/py-params/blob/master/LICENSE.txt>`_.

Install
-------

``params`` is on the Python Package Index (PyPI):

::

    pip install py-params


Usage
-----

``Params`` instances are ``dict`` s for which default values could be
provided as class level fields when subclassing `Params`.
Those default values could than be overridden in instances of the class,
by specifying the values in the constructor.

Accessing parameters not defined as class level variable
would raise an ``AttributeError``.

.. code:: python

    >>> from params import Params

    >>> class TestParams(Params):
    ...     param_a = 'a'
    ...     param_b = True

    >>> args=TestParams()                         ## using defaults
    >>> args
    {'param_a': 1, 'param_b': True}

    >>> TestParams(param_a='c')                   ## override param_a
    {'param_a': 'c', 'param_b': True}

    >>> args.param_a = 2                          ## access as attribute or key
    >>> args["param_a"] = 3
    >>> args.param_a == args["param_a"]
    True

    >>> args.param_c
    AttributeError: 'TestParams' object has no attribute 'test_c'

    >>> args.param_c = 3
    AttributeError: Setting unexpected parameter 'param_c' in Params instance 'TestParams'

    >>> args["param_d"] = 4
    AttributeError: Setting unexpected parameter 'param_d' in Params instance 'TestParams'



.. |Build Status| image:: https://travis-ci.org/kpe/py-params.svg?branch=master
   :target: https://travis-ci.org/kpe/py-params
.. |Coverage Status| image:: https://coveralls.io/repos/kpe/py-params/badge.svg?branch=master
   :target: https://coveralls.io/r/kpe/py-params
.. |Version Status| image:: https://badge.fury.io/py/py-params.svg
   :target: https://badge.fury.io/py/py-params
.. |Python Versions| image:: https://img.shields.io/pypi/pyversions/py-params.svg
.. |Downloads| image:: https://img.shields.io/pypi/dm/py-params.svg

Resources
---------

As an illustration of how ``Params`` could be used to reduce boilerplate code check:

- `kpe/params-flow`_  - utilities for reducing keras boilerplate code in custom layers
- `kpe/bert-for-tf2`_ - BERT implementation using the TensorFlow 2 Keras API

.. _`kpe/params-flow`: https://github.com/kpe/params-flow
.. _`kpe/bert-for-tf2`: https://github.com/kpe/bert-for-tf2

