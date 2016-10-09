# -*- coding: utf-8 -*-
"""写真の振る舞いの共通的な機能."""
import sys
import cv2
import exifread
import os.path
import time
from numpy import ndarray

from organize.base import Base
import organize.exception as exception


class Photo(Base):
    """写真基底クラス."""

    def __init__(self, filename: str):
        # 画像ファイル名
        self._filename = filename
        # 画像読み込み
        self._image = cv2.imread(filename)
        if self._image is None:
            raise exception.Photo_read_exception()
        # オリジナル画像の保存
        self._original = self._image
        # 読み込んだ画像をグレースケールに変換
        self._gray = cv2.cvtColor(self._image, cv2.COLOR_BGR2GRAY)
        # 初期設置
        self._filename = filename
        # デバッグモード(「python -d」で実行するとsys.flags.debugはTrueに設定される)
        self._debug = sys.flags.debug
        # Exi read
        self._exif_tags = self._exif_read()

    @property
    def filename(self) -> str:
        return self._filename

    @property
    def image(self) -> ndarray:
        return self._image

    @property
    def original(self) -> ndarray:
        return self._original

    @property
    def debug(self) -> bool:
        return self._debug

    @debug.setter
    def debug(self, value: str):
        if value.lower() == "true":
            self._debug = True
        else:
            self._debug = False

    def shooting_date(self) -> str:
        """EXIF撮影日.
        保持している写真の撮影日をEXIFから取得して返却.

        Args:
        return:
            撮影日 YYYY-MM-DD.
        """
        try:
            datetime = "%s" % self._exif_tags["EXIF DateTimeOriginal"]
            array = datetime.split(" ")
            date = array[0].replace(":", "-")
            return date
        except KeyError:
            raise exception.Photo_exif_read_exception

    def shooting_datetime(self) -> str:
        """EXIF撮影日時.
        保持している写真の撮影日時をEXIFから取得して返却.

        Args:
        return:
            撮影日時 YYYY/MM/DD HH:NN:SS.
        """
        try:
            datetime = "%s" % self._exif_tags["EXIF DateTimeOriginal"]
            array = datetime.split(" ")
            datetime = array[0].replace(":", "/") + " " + array[1]
            return datetime
        except KeyError:
            raise exception.Photo_exif_read_exception

    def resize(self, size: float):
        """画像のリサイズ.
        パーセントの値で指定された値で保持している画像をリサイズ

        Args:
            size: リサイズのパーセント指定(例:90.5)
        return:
        """
        width = self._image.shape[1] * (float(size) / 100)
        height = self._image.shape[0] * (float(size) / 100)
        self._image = cv2.resize(self._image, (int(width), int(height)))

    def edges(self):
        """画像に枠線を付与"""
        x = self._image.shape[1] - 1
        y = self._image.shape[0] - 1
        cv2.rectangle(self._image, (0, 0), (x, y), (230, 230, 230), 1)

    def save(self, filename: str):
        """ 保存.
        指定されたファイル名で保持指定イメージを保存.
        ファイルの作成日時は撮影日時を設定.

        Args:
            filename: 保存先のパスを含むファイル名.
        return:
        """
        try:
            # イメージをファイルに保存
            cv2.imwrite(filename, self._image)
            # テキストボックスの中身をdatetimeに直す
            create_date = time.strptime(self.shooting_datetime(), "%Y/%m/%d %H:%M:%S")
            update_date = time.strptime(self.shooting_datetime(), "%Y/%m/%d %H:%M:%S")
            times = (time.mktime(create_date), time.mktime(update_date))
            # ファイル作成日、更新日の設定
            os.utime(filename, times)
            # ファイル名を保存先のファイル名で更新
            self._filename = filename
        except Exception:
            raise exception.Photo_write_exception()

    def _exif_read(self) -> dict:
        """EXIFデータの読み込み.
        保持している画像のEXIFデータを返却.

        Args:
        return:
            EXIFデータ.
        """
        with open(self._filename, "rb") as f:
            return exifread.process_file(f)
