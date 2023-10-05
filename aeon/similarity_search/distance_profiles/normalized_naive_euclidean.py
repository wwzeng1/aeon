# -*- coding: utf-8 -*-
"""normalized_naive_euclidean_profile."""

__author__ = ["baraline"]

import numpy as np
from numba import njit

from aeon.distances import euclidean_distance
from aeon.similarity_search.distance_profiles._commons import (
    AEON_SIMSEARCH_STD_THRESHOLD,
    _get_input_sizes,
    _z_normalize_2D_series_with_mean_std,
)


def normalized_naive_euclidean_profile(X, Q, X_means, X_stds, Q_means, Q_stds):
    """
    Compute a euclidean distance profile in a brute force way.

    It computes the distance profiles between the input time series and the query using
    the euclidean distance. The search is made in a brute force way without any
    optimizations and can thus be slow.

    A distance profile between a (univariate) time series X_i = {x_1, ..., x_m}
    and a query Q = {q_1, ..., q_m} is defined as a vector of size $m-(l-1)$,
    such as P(X_i, Q) = {d(C_1, Q), ..., d(C_m-(l-1), Q)} with d the euclidean distance,
    and C_j = {x_j, ..., x_{j+(l-1)}} the j-th candidate subsequence of size l in X_i.

    Parameters
    ----------
    X: array shape (n_instances, n_channels, series_length)
        The input samples.

    Q : np.ndarray shape (n_channels, query_length)
        The query used for similarity search.

    Returns
    -------
    distance_profile : np.ndarray shape (n_instances, series_length - query_length + 1)
        The distance profile between Q and the input time series X.

    """
    # Make STDS inferior to the threshold to 1 to avoid division per 0 error.
    Q_stds[Q_stds < AEON_SIMSEARCH_STD_THRESHOLD] = 1
    X_stds[X_stds < AEON_SIMSEARCH_STD_THRESHOLD] = 1

    return _normalized_naive_euclidean_profile(X, Q, X_means, X_stds, Q_means, Q_stds)


@njit(cache=True, fastmath=True)
def _normalized_naive_euclidean_profile(X, Q, X_means, X_stds, Q_means, Q_stds):
    n_samples, n_channels, X_length, Q_length, search_space_size = _get_input_sizes(
        X, Q
    )
    # With Q_stds = 1, _Q will be an array of 0
    Q = _z_normalize_2D_series_with_mean_std(Q, Q_means, Q_stds)
    distance_profile = np.full((n_samples, search_space_size), 1e12)

    # Compute euclidean distance for all candidate in a "brute force" way
    for i_sample in range(n_samples):
        for i_candidate in range(search_space_size):
            # Extract and normalize the candidate
            _C = X[i_sample, :, i_candidate : i_candidate + Q_length]

            _C = _z_normalize_2D_series_with_mean_std(
                _C, X_means[i_sample, :, i_candidate], X_stds[i_sample, :, i_candidate]
            )
            distance_profile[i_sample, i_candidate] = euclidean_distance(Q, _C)
    return distance_profile