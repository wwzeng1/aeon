# -*- coding: utf-8 -*-
# The key string (i.e. 'euclidean') must be the same as the name in _registry

_expected_distance_results = {
    # Result structure:
    # [single value series, univariate series, multivariate series]
    "euclidean": [5.0, 2.6329864895136623, 7.093596608755006, 70.56413351420169],
    "erp": [5.0, 5.037672883414786, 20.724482073800456],
    "edr": [1.0, 0.6, 1.0],
    "lcss": [1.0, 0.09999999999999998, 1.0],
    "squared": [25.0, 6.932617853961479, 50.31911284774053, 499.6749760624051],
    "dtw": [25.0, 2.180365495972097, 47.59969618998147, 461.05467389005753],
    "ddtw": [0.0, 2.0884818837222006, 34.837800040564005],
    "wdtw": [12.343758137512241, 0.985380547171357, 21.265839226825413],
    "wddtw": [0.0, 1.0442409418611003, 17.418900020282003],
    "msm": [5.0, 6.828557434224288, None],
    "twe": [5.0, 11.548698748091073, 39.87793560457224],
}

_expected_distance_results_params = {
    # Result structure:
    # [univariate series, multivariate series]
    "dtw": [
        [3.088712375990371, 47.59969618998147],
    ],
    "erp": [
        [0.6648081862148058, 4.365472428062562],
        [5.279748833082764, 20.71830043391765],
    ],
    "edr": [
        [0.3, 0.3],
        [0.3, 1.0],
    ],
    "lcss": [
        [0.09999999999999998, 1.0],
        [0.30000000000000004, 1.0],
    ],
    "ddtw": [
        [2.683958998434711, 34.837800040564005],
        [2.180365495972097, 47.59969618998147],
    ],
    "wdtw": [
        [1.364177898415523, 21.265839226825413],
        [0.2643712293510365, 3.8171163209131693],
    ],
    "wddtw": [
        [1.3419794992173555, 17.418900020282003],
        [1.0901827479860484, 23.799848094990736],
        [0.39934168049275554, 4.394193388153649],
    ],
    "twe": [
        [5.260445939887447, 9.230959005394121],
        [10.16824892186273, 38.87793560457224],
        [14.469312584616958, 41.0046466591961],
        [11.548698748091073, 39.87793560457224],
    ],
}
