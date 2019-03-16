
Params
======

|Build Status| |Coverage Status| |Version Status|

A type safe dictionary class in python.


LICENSE
-------

MIT. See `License File <https://github.com/kpe/params/blob/master/LICENSE.txt>`_.

Install
-------

``params`` is on the Python Package Index (PyPI):

::

    pip install py-params


Usage
-----

``Param`` instances are ``dict`` s for which default values could be
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

    >>> params=TestParams()                       ## using defaults
    >>> params
    {'param_a': 1, 'param_b': True}

    >>> TestParams(param_a='c')                   ## override param_a
    {'param_a': 'c', 'param_b': True}

    >>> params.param_c
    AttributeError: 'TestParams' object has no attribute 'test_b'

    >>> params.param_c = 3
    AttributeError: Setting unexpected parameter 'param_c' in Params instance 'TestParams'

    >>> assert
    {'param_a': 3, 'param_b': True}


.. |Build Status| image:: https://travis-ci.org/kpe/params.svg?branch=master
   :target: https://travis-ci.org/kpe/params
.. |Coverage Status| image:: https://coveralls.io/repos/kpe/params/badge.svg?branch=master
   :target: https://coveralls.io/r/kpe/params
.. |Version Status| image:: https://badge.fury.io/py/py-params.svg
   :target: https://badge.fury.io/py/py-params

