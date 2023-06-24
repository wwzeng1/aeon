# -*- coding: utf-8 -*-
# The key string (i.e. 'euclidean') must be the same as the name in _registry

_expected_distance_results = {
    # Result structure:
    # [single value series, univariate series, multivariate series, dataset,
    #   unequal univariate, multivariate unequal, dataset unequal]
    "euclidean": [
        5.0,
        2.6329864895136623,
        7.093596608755006,
        2.3179478388647876,
        4.938969178714248,
    ],
    "erp": [
        5.0,
        5.037672883414786,
        20.724482073800456,
        5.16666987535642,
        18.353616712062177,
    ],
    "edr": [1.0, 0.6, 1.0, 0.4, 0.5],
    "lcss": [1.0, 0.1, 1.0, 0.0, 1.0],
    "squared": [
        25.0,
        6.932617853961479,
        50.31911284774053,
        5.37288218369794,
        24.39341654828929,
    ],
    "dtw": [
        25.0,
        2.180365495972097,
        47.59969618998147,
        4.360373075383168,
        44.86527164702194,
    ],
    "ddtw": [
        0.0,
        2.0884818837222006,
        34.837800040564005,
        3.6475610211489875,
        35.916981095128804,
    ],
    "wdtw": [
        12.343758137512241,
        0.985380547171357,
        21.265839226825413,
        2.0040890166976926,
        20.795690703034445,
    ],
    "wddtw": [
        0.0,
        0.9736009365730778,
        15.926194649221529,
        1.7031094916423124,
        16.967390011736825,
    ],
    "msm": [
        5.0,
        6.828557434224288,
        54.950486942429855,
        9.155720688607646,
        83.80645242153975,
    ],
    "twe": [
        5.0,
        11.33529624872385,
        40.346435059599386,
        12.461233755089522,
        36.0265974253265,
    ],
    "psi_dtw": [
        25.0,
        1.56684305619195,
        38.31787570257995,
        4.360373075383168,
        44.86527164702194,
    ],
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
        [7.399565602170839, 21.90092421200079],
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
    ],
    "wdtw": [
        [1.364177898415523, 21.265839226825413],
        [0.02752598656586074, 0.33677832093219406],
    ],
    "wddtw": [
        [1.223806382386346, 15.926194649221529],
        [0.08524969290653987, 0.663028083142974],
    ],
    "twe": [
        [4.045224987722827, 8.724529215084788],
        [8.892626757586168, 39.346435059599386],
        [14.469312584616958, 41.0046466591961],
    ],
    "psi_dtw": [
        [1.56684305619195, 38.31787570257995],
        [0.7475067384202918, 23.767777809820863],
    ],
}
