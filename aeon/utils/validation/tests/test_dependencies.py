#!/usr/bin/env python3 -u
# -*- coding: utf-8 -*-
"""Test functions in the _dependencies file."""

import pytest

# _check_dl_dependencies,; _check_python_version,
from aeon.utils.validation._dependencies import _check_soft_dependencies


def test__check_soft_dependencies():
    with pytest.raises(TypeError, match="packages must be str or tuple of str"):
        _check_soft_dependencies((1, 2, 3))
    with pytest.raises(TypeError, match="package_import_alias must be a dict"):
        _check_soft_dependencies((1, 2, 3))


# def test__check_dl_dependencies():
#    pass


# def test__check_python_version():
#    pass


def test__check_estimator_deps():
    pass
