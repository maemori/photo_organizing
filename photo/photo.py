# -*- coding: utf-8 -*-

""" 写真の振る舞いの共通的な機能.
 モジュールの視点ではファイルを統合した方が良い？.
"""

import cv2
import exifread
import os.path
import time

class Photo:
    """ 写真基底クラス
    """

    DEBUG_TEXT_Y = 80

    def __init__(self, filename):
        # 画像読み込み
        self._image = cv2.imread(filename)
        # オリジナル画像の保存
        self._original = self._image
        # 読み込んだ画像をグレースケールに変換
        self._gray = cv2.cvtColor(self._image, cv2.COLOR_BGR2GRAY)
        # 初期設置
        self._filename = filename
        # デバッグモード
        self._debug = False
        # Exi read
        self._exif_tags = self._exif_read()

    def __getattr__(self, item):
        if item == 'image':
            return self._image
        if item == 'original':
            return self._original
        elif item == 'debug':
            return self._debug
        else:
            raise AttributeError(item)

    def shooting_date(self):
        """ EXIF撮影日を返却

        :return: 撮影日 YYYY-MM-DD
        """
        datetime = '%s' % self._exif_tags['EXIF DateTimeOriginal']
        array = datetime.split(" ")
        date = array[0].replace(':', '-')
        return date

    def shooting_datetime(self):
        """ EXIF撮影日時を返却

        :return: 撮影日時 YYYY/MM/DD HH:NN:SS
        """
        datetime = '%s' % self._exif_tags['EXIF DateTimeOriginal']
        array = datetime.split(" ")
        datetime = array[0].replace(':', '/') + " " + array[1]
        return datetime

    def resize(self, size):
        """
        画像のリサイズ

        :rtype: object
        :param size:
        :return:
        """
        width = self._image.shape[1] * (float(size) / 100)
        hight = self._image.shape[0] * (float(size) / 100)
        """
        resize_image = cv2.resize(self._image, (int(hight), int(width)))
        return resize_image
        """
        self._image = cv2.resize(self._image, (int(width), int(hight)))

    def edges(self):
        x = self._image.shape[1] - 1
        y = self._image.shape[0] - 1
        cv2.rectangle(self._image, (0, 0), (x, y), (230, 230, 230), 1)

    def save(self, filename):
        """ 保存.
        指定されたファイル名で保持指定イメージを保存.
        ファイルの作成日時は撮影日時を設定.

        :param filename:
        :return:
        """
        try:
            # イメージをファイルに保存
            cv2.imwrite(filename, self._image)
            # テキストボックスの中身をdatetimeに直す
            create_date = time.strptime(self.shooting_datetime(), '%Y/%m/%d %H:%M:%S')
            update_date = time.strptime(self.shooting_datetime(), '%Y/%m/%d %H:%M:%S')
            times = (time.mktime(create_date), time.mktime(update_date))
            # ファイル作成日、更新日の設定
            os.utime(filename, times)
        except:
            raise

    def debug(self, value):
        if value.lower() == "true":
            self._debug = True
        else:
            self._debug = False

    def debug_text_y(self):
        ret = self.DEBUG_TEXT_Y
        self.DEBUG_TEXT_Y += Photo.DEBUG_TEXT_Y
        return ret

    def _exif_read(self):
        with open(self._filename, "rb") as f:
            return exifread.process_file(f)