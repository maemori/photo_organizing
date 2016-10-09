#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import shutil
import sys
import unittest
from numpy import ndarray

sys.path.append(os.pardir)
import organize.photo as photo
import organize.exception as exception
import everyone.util as util

import test_setting


class PhotoTest(unittest.TestCase):
    """Photo test class"""
    setting = test_setting.Setting()
    TEST_FILE_DIR = './resource/test_input_photo/set1'
    TARGET_FILE = os.path.join(setting.INPUT_DIR, '20160903_041533_000.jpg')
    EXIF_READ_NG_FILE = 'EXIF_NO_DATA.jpg'

    # テスト初期化時に実行
    @classmethod
    def setUpClass(cls):
        # テスト用入力ファイルの設置
        copy_func = util.files(util.copy, cls.TEST_FILE_DIR)
        copy_func(cls.setting.INPUT_DIR)

    # テスト終了時に実行
    @classmethod
    def tearDownClass(cls):
        pass

    # テストメソッド前処理
    def setUp(self):
        # オブジェクトの生成
        self.target = photo.Photo(self.TARGET_FILE)

    # テストメソッド後処理
    def tearDown(self):
        pass

    # 生成例外
    def test_init_exception(self):
        expected = 'Can not read the image file!'
        try:
            # テストターゲットの実行
            photo.Photo('NOT FILE')
        except exception.Photo_read_exception as ex:
            actual = repr(ex)
            self.assertEqual(expected, actual)
        else:
            self.assertTrue(False)

    # ファイ名の取得
    def test_get_filename(self):
        expected = self.TARGET_FILE
        # テストターゲットの実行
        actual = self.target.filename
        self.assertEqual(expected, actual)

    # オリジナル画像取得
    def test_get_original(self):
        # テストターゲットの実行
        actual = self.target.original
        self.assertTrue(isinstance(actual, ndarray))

    # 撮影日
    def test_shooting_date(self):
        expected = '2016-09-03'
        # テストターゲットの実行
        actual = self.target.shooting_date()
        self.assertEqual(expected, actual)

    # 撮影日時
    def test_shooting_datetime(self):
        expected = '2016/09/03 04:15:33'
        # テストターゲットの実行
        actual = self.target.shooting_datetime()
        self.assertEqual(expected, actual)

    # 画像のリサイズ
    def test_resize(self):
        expected = [
            [[79, 69, 70], [149, 136, 126]],
            [[34, 25, 21], [183, 195, 193]],
            [[32, 23, 20], [43, 31, 27]]
        ]
        # テストターゲットの実行
        self.target.resize(0.1)
        actual = self.target.image
        compare = (expected == actual.tolist())
        self.assertTrue(compare)

    # 画像に枠線を付与
    def test_edges(self):
        expected = [
            [[230, 230, 230], [230, 230, 230]],
            [[230, 230, 230], [230, 230, 230]],
            [[230, 230, 230], [230, 230, 230]]
        ]
        self.target.resize(0.1)
        # テストターゲットの実行
        self.target.edges()
        actual = self.target.image
        compare = (expected == actual.tolist())
        self.assertTrue(compare)

    # 保存
    def test_save(self):
        output_file = self.setting.OUTPUT_DIR + os.sep + 'output_file.jpg'
        # テストターゲットの実行
        self.target.save(output_file)
        compare = os.path.isfile(output_file)
        self.assertTrue(compare)

    # 保存例外
    def test_save_exception(self):
        expected = 'Failed to save photo!'
        output_file = ''
        try:
            # テストターゲットの実行
            self.target.save(output_file)
        except exception.Photo_write_exception as ex:
            actual = repr(ex)
            self.assertEqual(expected, actual)
        else:
            self.assertTrue(False)

    # デバッグの設定
    def test_set_debug_true(self):
        expected = True
        self.target.debug = 'TrUe'
        # テストターゲットの実行
        actual = self.target.debug
        self.assertEqual(expected, actual)

    # デバッグの設定
    def test_set_debug_False(self):
        expected = False
        self.target.debug = 'fALse'
        # テストターゲットの実行
        actual = self.target.debug
        self.assertEqual(expected, actual)

    # EXIF読み込み失敗 撮影日
    def test_shooting_date_exif_exception(self):
        expected = 'EXIF data can not be read!'
        try:
            # オブジェクトの生成
            target = photo.Photo(self.setting.INPUT_DIR + os.sep + self.EXIF_READ_NG_FILE)
            # テストターゲットの実行
            target.shooting_date()
        except exception.Photo_exif_read_exception as ex:
            actual = repr(ex)
            self.assertEqual(expected, actual)
        else:
            self.assertTrue(False)

    # EXIF読み込み失敗 撮影日時
    def test_shooting_datetime_exif_exception(self):
        expected = 'EXIF data can not be read!'
        try:
            # オブジェクトの生成
            target = photo.Photo(self.setting.INPUT_DIR + os.sep + self.EXIF_READ_NG_FILE)
            # テストターゲットの実行
            target.shooting_datetime()
        except exception.Photo_exif_read_exception as ex:
            actual = repr(ex)
            self.assertEqual(expected, actual)
        else:
            self.assertTrue(False)


if __name__ == '__main__':
    # unittestを実行
    unittest.main()
