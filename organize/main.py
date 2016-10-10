#!/usr/bin/env python
# -*- coding: utf-8 -*-

from organize.photos import Photos
import organize.exception as exception


def main():
    """写真整理の実行."""
    try:
        target = Photos()
        target.organize()
    except exception.Photo_exception:
        pass
