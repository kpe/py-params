#!/usr/bin/env python

#
# created by kpe on 16.03.2019 at 1:26 AM
#

from setuptools import setup, find_packages


with open("README.rst", "r") as fh:
    long_description = fh.read()

with open("version", "r") as fh:
    __version__ = fh.read().strip()

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
      zip_safe=True,
      python_requires=">=3.4",
      classifiers=[
          "Development Status :: 5 - Production/Stable",
          "License :: OSI Approved :: MIT License",
          "Programming Language :: Python",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.4",
          "Programming Language :: Python :: 3.5",
          "Programming Language :: Python :: 3.6",
          "Programming Language :: Python :: 3.7",
          "Programming Language :: Python :: Implementation :: CPython",
          "Programming Language :: Python :: Implementation :: PyPy"])
