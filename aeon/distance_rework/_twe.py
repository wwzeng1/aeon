import numpy as np
from numba import njit
from aeon.distance_rework._squared import univariate_squared_distance
from aeon.distance_rework._bounding_matrix import create_bounding_matrix


@njit(cache=True, fastmath=True)
def twe_distance(
        x: np.ndarray,
        y: np.ndarray,
        window=None,
        nu: float = 0.001,
        lmbda: float = 1.
) -> float:
    """Compute the TWE distance between two time series.

    Parameters
    ----------
    x: np.ndarray (n_dims, n_timepoints)
        First time series.
    y: np.ndarray (n_dims, n_timepoints)
        Second time series.
    window: int, defaults = None
        Window size. If None, the window size is set to the length of the
        shortest time series.
    nu: float, defaults = 0.001
        A non-negative constant which characterizes the stiffness of the elastic
        twe measure. Must be > 0.
    lmbda: float, defaults = 1.0
        A constant penalty that punishes the editing efforts. Must be >= 1.0.

    Returns
    -------
    float
        TWE distance between x and y.

    Examples
    --------
    >>> import numpy as np
    >>> from aeon.distance_rework import twe_distance
    >>> x = np.array([[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]])
    >>> y = np.array([[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]])
    >>> twe_distance(x, y)
    0.0
    """
    bounding_matrix = create_bounding_matrix(x.shape[1], y.shape[1], window)
    x = _pad_arrs(x)
    y = _pad_arrs(y)
    return _twe_distance(x, y, bounding_matrix, nu, lmbda)


#
# @njit(cache=True, fastmath=True)
def twe_cost_matrix(
        x: np.ndarray,
        y: np.ndarray,
        window=None,
        nu: float = 0.001,
        lmbda: float = 1.
) -> np.ndarray:
    """Compute the TWE cost matrix between two time series.

    Parameters
    ----------
    x: np.ndarray (n_dims, n_timepoints)
        First time series.
    y: np.ndarray (n_dims, n_timepoints)
        Second time series.
    window: int, defaults = None
        Window size. If None, the window size is set to the length of the
        shortest time series.
    nu: float, defaults = 0.001
        A non-negative constant which characterizes the stiffness of the elastic
        twe measure. Must be > 0.
    lmbda: float, defaults = 1.0
        A constant penalty that punishes the editing efforts. Must be >= 1.0.

    Returns
    -------
    np.ndarray (n_timepoints_x, n_timepoints_y)
        TWE cost matrix between x and y.

    Examples
    --------
    >>> import numpy as np
    >>> from aeon.distance_rework import twe_cost_matrix
    >>> x = np.array([[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]])
    >>> y = np.array([[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]])
    >>> twe_cost_matrix(x, y)
    array([[ 0.   ,  2.001,  4.002,  6.003,  8.004, 10.005, 12.006, 14.007,
            16.008, 18.009],
           [ 2.001,  0.   ,  2.001,  4.002,  6.003,  8.004, 10.005, 12.006,
            14.007, 16.008],
           [ 4.002,  2.001,  0.   ,  2.001,  4.002,  6.003,  8.004, 10.005,
            12.006, 14.007],
           [ 6.003,  4.002,  2.001,  0.   ,  2.001,  4.002,  6.003,  8.004,
            10.005, 12.006],
           [ 8.004,  6.003,  4.002,  2.001,  0.   ,  2.001,  4.002,  6.003,
             8.004, 10.005],
           [10.005,  8.004,  6.003,  4.002,  2.001,  0.   ,  2.001,  4.002,
             6.003,  8.004],
           [12.006, 10.005,  8.004,  6.003,  4.002,  2.001,  0.   ,  2.001,
             4.002,  6.003],
           [14.007, 12.006, 10.005,  8.004,  6.003,  4.002,  2.001,  0.   ,
             2.001,  4.002],
           [16.008, 14.007, 12.006, 10.005,  8.004,  6.003,  4.002,  2.001,
             0.   ,  2.001],
           [18.009, 16.008, 14.007, 12.006, 10.005,  8.004,  6.003,  4.002,
             2.001,  0.   ]])
    """
    bounding_matrix = create_bounding_matrix(x.shape[1], y.shape[1], window)
    x = _pad_arrs(x)
    y = _pad_arrs(y)
    return _twe_cost_matrix(x, y, bounding_matrix, nu, lmbda)


@njit(cache=True, fastmath=True)
def _twe_distance(
        x: np.ndarray,
        y: np.ndarray,
        bounding_matrix: np.ndarray,
        nu: float = 0.001,
        lmbda: float = 1.
) -> float:
    return _twe_cost_matrix(
        x, y, bounding_matrix, nu, lmbda
    )[x.shape[1] - 2, y.shape[1] - 2]


@njit(cache=True, fastmath=True)
def _twe_cost_matrix(
        x: np.ndarray,
        y: np.ndarray,
        bounding_matrix: np.ndarray,
        nu: float = 0.001,
        lmbda: float = 1.
) -> np.ndarray:
    x_size = x.shape[1]
    y_size = y.shape[1]
    cost_matrix = np.zeros((x_size, y_size))
    cost_matrix[0, 1:] = np.inf
    cost_matrix[1:, 0] = np.inf

    del_add = nu + lmbda

    for i in range(1, x_size):
        for j in range(1, y_size):
            if bounding_matrix[i - 1, j - 1]:
                # Deletion in x
                del_x_squared_dist = univariate_squared_distance(x[:, i - 1], x[:, i])
                del_x = cost_matrix[i - 1, j] + del_x_squared_dist + del_add
                # Deletion in y
                del_y_squared_dist = univariate_squared_distance(y[:, j - 1], y[:, j])
                del_y = cost_matrix[i, j - 1] + del_y_squared_dist + del_add

                # Match
                match_same_squared_d = univariate_squared_distance(x[:, i], y[:, j])
                match_prev_squared_d = univariate_squared_distance(x[:, i - 1],
                                                                   y[:, j - 1])
                match = (
                        cost_matrix[i - 1, j - 1]
                        + match_same_squared_d
                        + match_prev_squared_d
                        + nu * (abs(i - j) + abs((i - 1) - (j - 1)))
                )

                cost_matrix[i, j] = min(del_x, del_y, match)

    return cost_matrix[1:, 1:]


@njit(cache=True, fastmath=True)
def _pad_arrs(x: np.ndarray):
    padded_x = np.zeros((x.shape[0], x.shape[1] + 1))
    zero_arr = np.array([0.0])
    for i in range(x.shape[0]):
        padded_x[i, :] = np.concatenate((zero_arr, x[i, :]))
    return padded_x


@njit(cache=True, fastmath=True)
def twe_pairwise_distance(
        X: np.ndarray, window: float = None, epsilon: float = 1.
) -> np.ndarray:
    n_instances = X.shape[0]
    distances = np.zeros((n_instances, n_instances))
    bounding_matrix = create_bounding_matrix(X.shape[2], X.shape[2], window)

    # Pad the arrays before so that we dont have to redo every iteration
    padded_X = np.zeros((X.shape[0], X.shape[1], X.shape[2] + 1))
    for i in range(X.shape[0]):
        padded_X[i] = _pad_arrs(X[i])

    for i in range(n_instances):
        for j in range(i + 1, n_instances):
            distances[i, j] = _twe_distance(
                padded_X[i], padded_X[j], bounding_matrix, epsilon
            )
            distances[j, i] = distances[i, j]

    return distances


@njit(cache=True, fastmath=True)
def twe_from_single_to_multiple_distance(
        x: np.ndarray, y: np.ndarray, window: float = None, epsilon: float = 1.
):
    n_instances = y.shape[0]
    distances = np.zeros(n_instances)
    bounding_matrix = create_bounding_matrix(x.shape[1], y.shape[2], window)

    padded_x = _pad_arrs(x)

    for i in range(n_instances):
        distances[i] = _twe_distance(padded_x, _pad_arrs(y[i]), bounding_matrix, epsilon)

    return distances


@njit(cache=True, fastmath=True)
def twe_from_multiple_to_multiple_distance(
        x: np.ndarray, y: np.ndarray, window: float = None, epsilon: float = 1.
):
    n_instances = x.shape[0]
    m_instances = y.shape[0]
    distances = np.zeros((n_instances, m_instances))
    bounding_matrix = create_bounding_matrix(x.shape[2], y.shape[2], window)

    # Pad the arrays before so that we dont have to redo every iteration
    padded_x = np.zeros((x.shape[0], x.shape[1], x.shape[2] + 1))
    for i in range(x.shape[0]):
        padded_x[i] = _pad_arrs(x[i])

    padded_y = np.zeros((y.shape[0], y.shape[1], y.shape[2] + 1))
    for i in range(y.shape[0]):
        padded_y[i] = _pad_arrs(y[i])

    for i in range(n_instances):
        for j in range(m_instances):
            distances[i, j] = _twe_distance(
                padded_x[i], padded_y[j], bounding_matrix, epsilon
            )
    return distances
