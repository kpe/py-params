#!/bin/bash

PEP8_IGNORE=E221,E501,W504,W391

pep8 --ignore=${PEP8_IGNORE} --exclude=tests,.venv -r --show-source tests params

coverage run --source=params $(which nosetests) --with-doctest tests/
coverage report --show-missing --fail-under=100
