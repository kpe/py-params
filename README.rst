
Params
======

|Build Status| |Coverage Status| |Version Status| |Python Versions| |Downloads|

A type safe dict utility class in python.


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

``Params`` represents a set of parameters modeled as a ``dict`` with a fixed set of keys.
Default values are provided as class level attributes in ``Params`` subclasses.
Parameter values can then be specified when constructing a ``Params`` instance overriding the default values.
The parameter values can then be accessed both as attributes and ``dict`` items,
however the ``Params`` instance key set is closed for modification
thus an exception is raised when a parameter name is misspelled.

Accessing parameters not defined as class level attributes would raise an ``AttributeError``.

.. code:: python

    >>> import params as pp

    >>> class TestParams(pp.Params):
    ...     param_a = 1
    ...     param_b = True

    >>> params = TestParams()                     ## using the defaults
    >>> params
    {'param_a': 1, 'param_b': True}

    >>> TestParams(param_a=2)                     ## setting a value for param_a
    {'param_a': 2, 'param_b': True}

    >>> params.param_a = 3                          ## access as attribute or key
    >>> params["param_a"] = 4
    >>> params.param_a == params["param_a"]
    True

    >>> params.param_c
    AttributeError: 'TestParams' object has no attribute 'test_c'

    >>> params.param_c = 3
    AttributeError: Setting unexpected parameter 'param_c' in Params instance 'TestParams'

    >>> params["param_d"] = 4
    AttributeError: Setting unexpected parameter 'param_d' in Params instance 'TestParams'

``Params`` instances can be used to generate CLI parser with ``argparse``:

.. code:: python

    >>> import params as pp

    >>> class TestParams(pp.Params):
    ...     number_of_things = pp.Param(None, doc="Specifies the number of things", dtype=int, required=True)
    ...     use_feature_x    = pp.Param(True, doc="whether to use feature X")
    >>> parser = TestParams.to_argument_parser()
    >>> parser.print_help()
    usage: pydevconsole.py [-h] --number-of-things NUMBER_OF_THINGS
                           [--use-feature-x [USE_FEATURE_X]]

    optional arguments:
      -h, --help            show this help message and exit
      --number-of-things NUMBER_OF_THINGS
                            Specifies the number of things
      --use-feature-x [USE_FEATURE_X]
                            whether to use feature X
    >>> args = parser.parse_known_args(["--number-of-things", "7"])
    >>> TestParams(args._get_kwargs())
    {'number_of_things': 7, 'use_feature_x': True}


.. |Build Status| image:: https://travis-ci.org/kpe/py-params.svg?branch=master
   :target: https://travis-ci.org/kpe/py-params
.. |Coverage Status| image:: https://coveralls.io/repos/kpe/py-params/badge.svg?branch=master
   :target: https://coveralls.io/r/kpe/py-params
.. |Version Status| image:: https://badge.fury.io/py/py-params.svg
   :target: https://badge.fury.io/py/py-params
.. |Python Versions| image:: https://img.shields.io/pypi/pyversions/py-params.svg
.. |Downloads| image:: https://img.shields.io/pypi/dm/py-params.svg


NEWS
----
 - **04.Apr.2020** - ``WithParams`` mixin added.
 - **31.Mar.2020** - support for generating ``argparse`` CLI parser. Hierarchy aggregation refactored.


Resources
---------

As an illustration of how ``Params`` could be used to reduce boilerplate code check:

- `kpe/params-flow`_  - utilities for reducing keras boilerplate code in custom layers
- `kpe/bert-for-tf2`_ - BERT implementation using the TensorFlow 2 Keras API

.. _`kpe/params-flow`: https://github.com/kpe/params-flow
.. _`kpe/bert-for-tf2`: https://github.com/kpe/bert-for-tf2

