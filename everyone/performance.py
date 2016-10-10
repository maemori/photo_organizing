# -*- coding: utf-8 -*-
"""パフォーマンスに関する処理"""
from time import time

import everyone.log as log


def time_func(func):
    """処理時間計測を自動化するデコレータ."""
    performance_log = log.logger("performance")

    def measure_time(*args, **kwargs):
        start_time = time()
        result = func(*args, **kwargs)
        end_time = time()
        processing_time = end_time - start_time
        performance_log.info(
            "processing time (seconds) - {0:s} - {1:.5f}".format(func.__name__, processing_time))
        return result
    return measure_time
