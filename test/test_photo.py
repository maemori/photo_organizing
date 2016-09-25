#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import unittest

from numpy import ndarray

sys.path.append(os.pardir)
import organizing.photo as photo
import organizing.exception as exception
import organizing.util as util


class PhotoTest(unittest.TestCase):
    """Photo test class"""
    TEST_FILE_DIR = './test_data/resource/input_photo'
    INPUT_DIR = './input_photo'
    OUTPUT_DIR = './output_public_photo'
    TARGET_FILE = './input_photo/20160903_041533_000.jpg'

    # テスト初期化時に実行
    @classmethod
    def setUpClass(cls):
        # テスト用入力ファイルの設置
        copy_func = util.photo_files(util.copy, cls.TEST_FILE_DIR)
        copy_func(cls.INPUT_DIR)

    # テスト終了時に実行
    @classmethod
    def tearDownClass(cls):
        # デバッグモード時はテスト結果の画像を削除しない
        if not sys.flags.debug:
            # テスト用入力ファイルを削除
            input_file_delete_func = util.photo_files(util.delete, cls.INPUT_DIR)
            input_file_delete_func()
            # テスト用出力ファイルを削除
            output_file_delete_func = util.photo_files(util.delete, cls.OUTPUT_DIR)
            output_file_delete_func()

    # テストメソッド前処理
    def setUp(self):
        self.target = photo.Photo(self.TARGET_FILE)

    # テストメソッド後処理
    def tearDown(self):
        pass

    # 生成例外
    def test_init_exception(self):
        expected = 'Can not read the image file!'
        try:
            target = photo.Photo('NOT FILE')
        except exception.Photo_read_exception as ex:
            actual = repr(ex)
            self.assertEqual(expected, actual)
        else:
            self.assertTrue(False)

    # オリジナル画像取得
    def test_get_original(self):
        result = self.target.original
        self.assertTrue(isinstance(result, ndarray))

    # 撮影日
    def test_shooting_date(self):
        expected = '2016-09-03'
        actual = self.target.shooting_date()
        self.assertEqual(expected, actual)

    # 撮影日時
    def test_shooting_datetime(self):
        expected = '2016/09/03 04:15:33'
        actual = self.target.shooting_datetime()
        self.assertEqual(expected, actual)

    # 画像のリサイズ
    def test_resize(self):
        expected = [
            [[79, 69, 70], [149, 136, 126]],
            [[34, 25, 21], [183, 195, 193]],
            [[32, 23, 20], [43, 31, 27]]
        ]
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
        self.target.edges()
        actual = self.target.image
        compare = (expected == actual.tolist())
        self.assertTrue(compare)

    # 保存
    def test_save(self):
        output_file = self.OUTPUT_DIR + os.sep + 'output_file.jpg'
        self.target.save(output_file)
        compare = os.path.isfile(output_file)
        self.assertTrue(compare)

    # 保存例外
    def test_save_exception(self):
        expected = 'Failed to save photo!'
        output_file = ''
        try:
            self.target.save(output_file)
        except exception.Photo_write_exception as ex:
            actual = repr(ex)
            self.assertEqual(expected, actual)
        else:
            self.assertTrue(False)

    # 画像に付与するデバッグ情報の出力位置
    def test_debug_text_y(self):
        expected = 160
        actual = self.target.debug_text_y()
        actual = self.target.debug_text_y()
        self.assertEqual(expected, actual)

    # デバッグの設定
    def test_set_debug_true(self):
        expected = True
        self.target.debug = 'TrUe'
        actual = self.target.debug
        self.assertEqual(expected, actual)

    # デバッグの設定
    def test_set_debug_False(self):
        expected = False
        self.target.debug = 'fALse'
        actual = self.target.debug
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    # unittestを実行
    unittest.main()
