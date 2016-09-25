# -*- coding: utf-8 -*-
"""例外定義"""


class Photo_exception(Exception):
    """例外基底クラス."""
    pass


class Photo_read_exception(Photo_exception):
    """画像ファイル読み込み例外クラス."""
    def __repr__(self):
        return 'Can not read the image file!'


class Photo_write_exception(Photo_exception):
    """画像ファイル保存例外クラス."""
    def __repr__(self):
        return 'Failed to save photo!'


class Photo_cascade_exception(Photo_exception):
    """画像ファイル顔認識例外クラス."""
    def __repr__(self):
        return 'Fail to recognize the face!'
