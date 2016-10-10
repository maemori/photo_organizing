# -*- coding: utf-8 -*-
"""ログ出力"""
import yaml
from logging import config, getLogger


def logger(name=""):
    """ロガーの返却."""
    config.dictConfig(yaml.load(open("./conf/logging.yaml", encoding='UTF-8').read()))
    logger_process = getLogger(name)
    return logger_process
