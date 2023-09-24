# -*- coding: utf-8 -*-
"""Unit tests for clusterer deep learning base class functionality."""
import gc
import os
import time

import numpy as np
import pytest

from aeon.clustering.deep_learning.base import BaseDeepClusterer
from aeon.utils._testing.collection import make_2d_test_data
from aeon.utils.validation._dependencies import _check_soft_dependencies

__author__ = ["achieveordie", "hadifawaz1999"]


class _DummyDeepClusterer(BaseDeepClusterer):
    """Dummy Deep Clusterer for testing empty base deep class save utilities."""

    def __init__(self, last_file_name):
        self.last_file_name = last_file_name
        super(_DummyDeepClusterer, self).__init__(
            n_clusters=2, last_file_name=last_file_name
        )

    def build_model(self, input_shape):
        import tensorflow as tf

        input_layer_encoder = tf.keras.layers.Input(input_shape)
        gap = tf.keras.layers.GlobalAveragePooling1D()(input_layer_encoder)
        output_layer_encoder = tf.keras.layers.Dense(units=10)(gap)
        encoder = tf.keras.models.Model(
            inputs=input_layer_encoder, outputs=output_layer_encoder
        )

        input_layer_decoder = tf.keras.layers.Input((10,))
        dense = tf.keras.layers.Dense(10)(input_layer_decoder)
        _output_layer_decoder = tf.keras.layers.Dense(np.prod(input_shape))(dense)
        output_layer_decoder = tf.keras.layers.Reshape(target_shape=input_shape)(
            _output_layer_decoder
        )

        decoder = tf.keras.models.Model(
            inputs=input_layer_decoder, outputs=output_layer_decoder
        )

        input_layer = tf.keras.layers.Input(input_shape)
        encoder_ouptut = encoder(input_layer)
        decoder_output = decoder(encoder_ouptut)

        model = tf.keras.models.Model(inputs=input_layer, outputs=decoder_output)

        model.compile(loss="mse")

        return model

    def _fit(self, X, y=None):
        X = X.transpose(0, 2, 1)

        self.input_shape_ = X.shape[1:]
        self.model_ = self.build_model(self.input_shape_)

        self.history = self.model_.fit(
            X,
            X,
            batch_size=16,
            epochs=2,
        )

        gc.collect()
        return self

    def _score(self, X, y=None):
        return True


@pytest.mark.skipif(
    not _check_soft_dependencies("tensorflow", severity="none"),
    reason="skip test if required soft dependency not available",
)
def test_dummy_deep_clusterer():
    last_file_name = str(time.time_ns())

    # create a dummy deep classifier
    dummy_deep_clr = _DummyDeepClusterer(last_file_name=last_file_name)

    # generate random data

    X, _ = make_2d_test_data()

    # test fit function on random data
    dummy_deep_clr.fit(X=X)

    # test save last model to file than delete it

    dummy_deep_clr.save_last_model_to_file()

    os.remove("./" + last_file_name + ".hdf5")

    # test summary of model

    assert dummy_deep_clr.summary() is not None