#!/usr/bin/env python
# -*- coding: utf-8 -*-
import filecmp
import os
import sys
import unittest
import shutil

from numpy import ndarray

sys.path.append(os.pardir)
import organizing.cleaning as photo
import organizing.exception as exception
import organizing.util as util


class PhotoTest(unittest.TestCase):
    """Photo test class"""
    TEST_FILE_DIR = './test_data/resource/input_photo/set2'
    INPUT_DIR = './input_photo'
    OUTPUT_DIR = './output_public_photo'
    CASCADE_ORIGINAL_DIR = '../cascade'
    CASCADE_TEST_DIR = './cascade'
    TARGET_FILE_01 = './input_photo/20160803_105354_000.jpg'
    TARGET_FILE_02 = './input_photo/20160803_105426_000.jpg'
    TARGET_FILE_03 = './input_photo/20160803_105458_000.jpg'
    TARGET_FILE_04 = './input_photo/20160803_105530_000.jpg'
    TARGET_FILE_05 = './input_photo/20160803_105602_000.jpg'
    TARGET_FILE_06 = './input_photo/20160803_110727_000.jpg'
    TARGET_FILE_07 = './input_photo/20160803_110935_000.jpg'
    TARGET_FILE_08 = './input_photo/20160803_111247_000.jpg'
    TARGET_FILE_09 = './input_photo/20160803_111559_000.jpg'
    TARGET_FILE_10 = './input_photo/20160803_111631_000.jpg'
    TARGET_FILE_11 = './input_photo/20160803_111703_000.jpg'
    TARGET_FILE_12 = './input_photo/20160803_111839_000.jpg'
    TARGET_FILE_13 = './input_photo/20160803_111911_000.jpg'

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
        # カスケードファイルの設置
        cascade_func = util.files(util.copy, self.CASCADE_ORIGINAL_DIR)
        cascade_func(self.CASCADE_TEST_DIR)

    # テストメソッド後処理
    def tearDown(self):
        # カスケードファイルの削除
        cascade_func = util.files(util.delete, self.CASCADE_TEST_DIR)
        cascade_func()

    # ピンボケ判定 ピンボケ
    def test_out_of_focus_true(self):
        self.target = photo.Cleaning(self.TARGET_FILE_01)
        self.target.debug = 'True'
        actual = self.target.out_of_focus(30.0)
        self.target.save(self.OUTPUT_DIR + os.sep + 'test_out_of_focus_true.jpg')
        self.assertTrue(actual)

    # ピンボケ判定 ピンボケ
    def test_out_of_focus_false(self):
        self.target = photo.Cleaning(self.TARGET_FILE_03)
        self.target.debug = 'True'
        actual = self.target.out_of_focus(30.0)
        self.target.save(self.OUTPUT_DIR + os.sep + 'test_out_of_focus_false.jpg')
        self.assertTrue(not actual)

    # ピンボケ判定 判定結果取得
    def test_out_of_focus_get_status(self):
        self.target = photo.Cleaning(self.TARGET_FILE_01)
        self.target.debug = 'True'
        self.target.out_of_focus(30.0)
        actual = self.target.blurry_status
        self.target.save(self.OUTPUT_DIR + os.sep + 'test_out_of_focus_true.jpg')
        self.assertTrue(actual)

    # 画像の類似度判定 似ている
    def test_compare_true(self):
        self.target1 = photo.Cleaning(self.TARGET_FILE_07)
        self.target1.debug = 'True'
        self.target2 = photo.Cleaning(self.TARGET_FILE_07)
        actual = self.target1.compare(self.target2.original, 80.0)
        self.target1.save(self.OUTPUT_DIR + os.sep + 'test_compare_true.jpg')
        self.assertTrue(actual)

    # 画像の類似度判定 似ていない
    def test_compare_false(self):
        self.target1 = photo.Cleaning(self.TARGET_FILE_07)
        self.target1.debug = 'True'
        self.target2 = photo.Cleaning(self.TARGET_FILE_08)
        actual = self.target1.compare(self.target2.original, 80.0)
        self.target1.save(self.OUTPUT_DIR + os.sep + 'test_compare_false.jpg')
        self.assertTrue(not actual)

    # 画像の類似度判定 判定結果取得
    def test_compare_get_status(self):
        self.target1 = photo.Cleaning(self.TARGET_FILE_07)
        self.target1.debug = 'True'
        self.target2 = photo.Cleaning(self.TARGET_FILE_07)
        self.target1.compare(self.target2.original, 80.0)
        self.target1.save(self.OUTPUT_DIR + os.sep + 'test_compare_true.jpg')
        actual = self.target1.compare_status
        self.assertTrue(actual)

    # モザイク例外(設定情報なし)
    def test_mosaic_setting_exception(self):
        expected = 'Fail to recognize the face!'
        try:
            self.target = photo.Cleaning(self.TARGET_FILE_01)
            self.target._config.clear()
            self.target.mosaic()
        except exception.Photo_cascade_exception as ex:
            actual = repr(ex)
            self.assertEqual(expected, actual)
        else:
            self.assertTrue(False)

    # モザイク例外(カスケードファイルなし)
    def test_mosaic_not__file_exception(self):
        expected = 'Fail to recognize the face!'
        try:
            self.target = photo.Cleaning(self.TARGET_FILE_01)
            cascade_func = util.files(util.delete, self.CASCADE_TEST_DIR)
            cascade_func()
            self.target.mosaic()
        except exception.Photo_cascade_exception as ex:
            actual = repr(ex)
            self.assertEqual(expected, actual)
        else:
            self.assertTrue(False)

    # モザイク
    def test_mosaic(self):
        self.target = photo.Cleaning(self.TARGET_FILE_01)
        self.target.debug = 'True'
        self.target.mosaic()
        output_file = self.OUTPUT_DIR + os.sep + 'test_mosaic.jpg'
        self.target.save(output_file)
        compare = os.path.isfile(output_file)
        self.assertTrue(compare)


if __name__ == '__main__':
    # unittestを実行
    unittest.main()
