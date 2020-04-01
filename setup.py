#!/usr/bin/env python

#
# created by kpe on 16.03.2019 at 1:26 AM
#

from setuptools import setup, find_packages, convert_path

with open("README.rst", "r") as fh:
    long_description = fh.read()


def _version():
    ns = {}
    with open(convert_path("params/version.py"), "r") as fh:
        exec(fh.read(), ns)
    return ns['__version__']


__version__ = _version()


setup(name="py-params",
      version=__version__,
      url="https://github.com/kpe/py-params/",
      description="A type safe dictionary in python",
      long_description=long_description,
      long_description_content_type="text/x-rst",
      keywords="dict dictionary utility parameters flags arguments",
      license="MIT",
      author="kpe",
      author_email="kpe.git@gmailbox.org",
      packages=find_packages(exclude=["tests"]),

      include_package_data=True,
      zip_safe=False,
      python_requires=">=3.6",
      classifiers=[
          "Development Status :: 5 - Production/Stable",
          "License :: OSI Approved :: MIT License",
          "Programming Language :: Python",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.6",
          "Programming Language :: Python :: 3.7",
          "Programming Language :: Python :: 3.8",
          "Programming Language :: Python :: Implementation :: CPython",
          "Programming Language :: Python :: Implementation :: PyPy"])
