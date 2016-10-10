# -*- coding: utf-8 -*-
"""例外定義."""


class Photo_exception(Exception):
    """例外基底クラス."""
    def __repr__(self):
        return "Photo organizing exception!"


class Photo_read_exception(Photo_exception):
    """画像ファイル読み込み例外クラス."""
    def __repr__(self):
        return "Can not read the image file!"


class Photo_write_exception(Photo_exception):
    """画像ファイル保存例外クラス."""
    def __repr__(self):
        return "Failed to save photo!"


class Photo_exif_read_exception(Photo_exception):
    """画像ファイル保存例外クラス."""
    def __repr__(self):
        return "EXIF data can not be read!"


class Photo_setting_exception(Photo_exception):
    """設定ファイル読み込み例外クラス."""
    def __repr__(self):
        return "Failed to read the configuration file!"


class Photo_cascade_exception(Photo_exception):
    """画像ファイル顔認識例外クラス."""
    def __repr__(self):
        return "Fail to recognize the face!"


class Photo_thumbnail_exception(Photo_exception):
    """サムネイル画像作成例外クラス."""
    def __repr__(self):
        return "It failed to create a thumbnail image!"
