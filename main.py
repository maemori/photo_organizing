#!/usr/bin/env python
# -*- coding: utf-8 -*-

import photo.photos

if __name__ == '__main__':
    output_dirs = photo.photos.main()
    photo.photos.thumbnail(output_dirs)
    photo.photos.move_files()