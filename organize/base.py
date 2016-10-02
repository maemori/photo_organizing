# -*- coding: utf-8 -*-
"""基底クラス"""
import everyone.log as log


class Base:
    log = log.logger(__name__)
    log.info("Class load")
