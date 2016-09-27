#!/usr/bin/env python
# -*- coding: utf-8 -*-

from organize.photos import Photos
import organize.exception as exception

try:
    target = Photos()
    target.organize()
except exception.Photo_exception as ex:
    print('ERROR')
    print(' type:' + str(type(ex)))
    print(' args:' + str(ex.args))
    print(' exception:' + str(ex))
