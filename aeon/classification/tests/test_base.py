# -*- coding: utf-8 -*-
"""Unit tests for classifier base class functionality."""

import numpy as np
import numpy.random
import pandas as pd
import pytest

from aeon.classification import DummyClassifier
from aeon.classification.base import BaseClassifier, _get_metadata
from aeon.utils.validation.collection import COLLECTIONS_DATA_TYPES
from aeon.utils.validation.tests.test_collection import (
    EQUAL_LENGTH_UNIVARIATE,
    UNEQUAL_LENGTH_DATA_EXAMPLES,
)

__author__ = ["mloning", "fkiraly", "TonyBagnall", "MatthewMiddlehurst", "achieveordie"]

"""
 Need to test:
    1. base class fit, predict and predict_proba wortk with valid input
    2. checkX
    3. _get_metadata
    4. _check_y

"""


class _TestClassifier(BaseClassifier):
    """Cassifier for testing base class fit/predict/predict_proba."""

    def _fit(self, X, y):
        """Fit dummy."""
        return self

    def _predict(self, X):
        """Predict dummy."""
        return np.zeros(shape=(len(X),))

    def _predict_proba(self, X):
        """Predict proba dummy."""
        return np.zeros(shape=(len(X), 2))


class _TestHandlesAllInput(BaseClassifier):
    """Dummy classifier for testing base class fit/predict/predict_proba."""

    _tags = {
        "capability:multivariate": True,
        "capability:unequal_length": True,
        "capability:missing_values": True,
        "X_inner_mtype": ["np-list", "numpy3D"],
    }

    def _fit(self, X, y):
        """Fit dummy."""
        return self

    def _predict(self, X):
        """Predict dummy."""
        return self

    def _predict_proba(self, X):
        """Predict proba dummy."""
        return self


multivariate_message = r"multivariate series"
missing_message = r"missing values"
unequal_message = r"unequal length series"
incorrect_X_data_structure = r"must be a np.ndarray or a pd.Series"
incorrect_y_data_structure = r"must be 1-dimensional"


@pytest.mark.parametrize("data", COLLECTIONS_DATA_TYPES)
def test_base_classifier(data):
    """Test basic functionality with valid input for the BaseClassifier."""
    dummy = _TestClassifier()
    X = EQUAL_LENGTH_UNIVARIATE[data]
    y = np.array([0, 0, 0, 0, 0, 1, 1, 1, 1, 1])
    result = dummy.fit(X, y)
    # Fit returns self
    assert result is dummy
    preds = dummy.predict(X)
    assert isinstance(preds, np.ndarray)
    assert len(preds) == 10
    preds = dummy.predict_proba(X)
    assert preds.shape == (10, 2)


@pytest.mark.parametrize("data", COLLECTIONS_DATA_TYPES)
def test__get_metadata(data):
    X = EQUAL_LENGTH_UNIVARIATE[data]
    meta = _get_metadata(X)
    assert not meta["multivariate"]
    assert not meta["missing_values"]
    assert not meta["unequal_length"]
    assert meta["n_cases"] == 10


@pytest.mark.parametrize("data", COLLECTIONS_DATA_TYPES)
def test_convertX(data):
    """Directly test the conversions."""


@pytest.mark.parametrize("data", COLLECTIONS_DATA_TYPES)
def test_unequal(data):
    y = np.array([0, 0, 0, 0, 0, 1, 1, 1, 1, 1])
    if data in UNEQUAL_LENGTH_DATA_EXAMPLES.keys():
        all = _TestHandlesAllInput()
        #        none = _TestClassifier()
        all.fit(data, y)


#        assert dummy = _TestClassifier() fails


def test_classifier_score():
    """Test the base class score() function."""
    X = np.random.random(size=(6, 10))
    y = np.array([0, 0, 0, 1, 1, 1])
    dummy = DummyClassifier()
    dummy.fit(X, y)
    assert dummy.score(X, y) == 0.5
    y2 = pd.Series([0, 0, 0, 1, 1, 1])
    dummy.fit(X, y2)
    assert dummy.score(X, y) == 0.5
    assert dummy.score(X, y2) == 0.5


def test_predict_single_class():
    """Test return of predict predict_proba in case only single class seen in fit."""
    trainX = np.ones(shape=(10, 20))
    y = np.ones(10)
    testX = np.ones(shape=(10, 20))
    clf = DummyClassifier()
    clf.fit(trainX, y)
    y_pred = clf.predict(testX)
    y_pred_proba = clf.predict_proba(testX)
    assert y_pred.ndim == 1
    assert y_pred.shape == (10,)
    assert all(list(y_pred == 1))
    assert y_pred_proba.ndim == 2
    assert y_pred_proba.shape == (10, 1)
    assert all(list(y_pred_proba == 1))
