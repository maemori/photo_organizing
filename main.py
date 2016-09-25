#!/usr/bin/env python
# -*- coding: utf-8 -*-

import organizing.photos

output_dirs = organizing.photos.main()
organizing.photos.thumbnail(output_dirs)
organizing.photos.move_files()
