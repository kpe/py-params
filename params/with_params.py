# coding=utf-8
#
# created by kpe on 03.04.2020 at 6:02 PM
#

from __future__ import division, absolute_import, print_function

import params as pp


class WithParams:
    """
    Defines an abstract/base class/mixin for ``Params`` configured hierarchies.

    As ``WithParams.__init__()`` takes care for initializing the ``Params`` instance,
    building class hierarchies  utilizing the ``Params`` style of passing parameters,
    is done by overriding ``WithParams._construct()`` instead of ``__init__()``.

    Check ``tests/test_with_params.py`` for complete example.

    Usage:

      import params as pp

      class MyConfigurableClass(WithParams, BaseClass):
        class Params(pp.Params):
          cool_parameter = "configurable parameter"

        def _construct(*args, **kwargs):
          super()._construct(*args, **kwargs)  # calling BaseClass.__init__(*args, **kwargs)
          print(f"constructed with {args} and {self.params})

      inst = MyConfigurableClass("base_arg", base_kwarg="val", cool_parameter="val")

    """
    class Params(pp.Params):

        def create(self, *args, **kwargs):
            """ Creates a new WithParams instance by optional overriding the Params with kwargs. """
            return self.__class__._outer_class_.from_params(self, *args, **kwargs)

    def __init_subclass__(cls, **kwargs):
        cls.Params._outer_class_ = cls

    def __init__(self, *args, **kwargs):
        self._params, other_args = self.__class__.Params.from_dict(kwargs)
        self._construct(*args, **other_args)

    def _construct(self, *args, **kwargs):
        """Override this method instead of __init__ for construction."""
        super().__init__(*args, **kwargs)

    @property
    def params(self) -> Params:
        return self._params

    @classmethod
    def from_params(cls, params: Params, *args, **kwargs):
        """
        Creates an instance from the specified parameters (by overriding the params argument with kwargs).
        """
        # split non Params kwargs
        kwargs, other_args = cls.Params.from_dict(kwargs, return_unused=True, return_instance=False)
        kwargs = dict(cls.Params.from_dict(
            params, return_unused=False).clone(**kwargs))   # override with kwargs
        kwargs.update(**other_args)                         # add non Params kwargs back
        instance = cls(*args, **kwargs)
        return instance
