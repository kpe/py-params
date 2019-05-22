#!/usr/bin/env python

#
# created by kpe on 16.03.2019 at 1:26 AM
#


from setuptools import setup

import params


with open("README.rst", "r") as fh:
    long_description = fh.read()


setup(name='py-params',
      version=params.__version__,
      description='A type safe dictionary in python',
      url='https://github.com/kpe/py-params/',
      author='kpe',
      author_email='kpe.git@gmailbox.org',
      license='MIT',
      keywords='dictionary utility parameters flags',
      packages=['params'],
      package_data={'params': ['tests/*.py']},
      long_description=long_description,
      long_description_content_type="text/x-rst",
      zip_safe=False,
      python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
      classifiers=[
          "Development Status :: 5 - Production/Stable",
          "License :: OSI Approved :: MIT License",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.4",
          "Programming Language :: Python :: 3.5",
          "Programming Language :: Python :: 3.6",
          "Programming Language :: Python :: 3.7",
          "Programming Language :: Python :: Implementation :: CPython",
          "Programming Language :: Python :: Implementation :: PyPy"])
