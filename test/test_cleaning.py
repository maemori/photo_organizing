#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import shutil
import sys
import unittest

sys.path.append(os.pardir)
import organize.cleaning as photo
import organize.exception as exception
import everyone.util as util


class PhotoTest(unittest.TestCase):
    """Photo test class"""
    TEST_FILE_DIR = './resource/input_photo/set2'
    TEST_DIR = './photo'
    INPUT_DIR = TEST_DIR + os.sep + 'input'
    OUTPUT_DIR = TEST_DIR + os.sep + 'public'
    CASCADE_ORIGINAL_DIR = '../cascade'
    CASCADE_TEST_DIR = './cascade/'
    TARGET_FILE_01 = INPUT_DIR + os.sep + '20160803_105354_000.jpg'
    TARGET_FILE_02 = INPUT_DIR + os.sep + '20160803_105458_000.jpg'
    TARGET_FILE_03 = INPUT_DIR + os.sep + '20160803_110935_000.jpg'
    TARGET_FILE_04 = INPUT_DIR + os.sep + '20160803_111247_000.jpg'

    # テスト初期化時に実行
    @classmethod
    def setUpClass(cls):
        try:
            # テスト用ディレクトリの設置
            os.makedirs(cls.INPUT_DIR)
            os.makedirs(cls.OUTPUT_DIR)
            os.makedirs(cls.CASCADE_TEST_DIR)
        except OSError:
            pass
        # テスト用入力ファイルの設置
        copy_func = util.files(util.copy, cls.TEST_FILE_DIR)
        copy_func(cls.INPUT_DIR)

    # テスト終了時に実行
    @classmethod
    def tearDownClass(cls):
        # デバッグモード時はテスト結果の画像を削除しない
        if not sys.flags.debug:
            # テスト用ディレクトリの削除
            shutil.rmtree(cls.TEST_DIR)
            shutil.rmtree(cls.CASCADE_TEST_DIR)

    # テストメソッド前処理
    def setUp(self):
        # カスケードファイルの設置
        cascade_func = util.files(util.copy, self.CASCADE_ORIGINAL_DIR)
        test = cascade_func(self.CASCADE_TEST_DIR)
        print(test)

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
        self.target = photo.Cleaning(self.TARGET_FILE_02)
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
        self.target1 = photo.Cleaning(self.TARGET_FILE_03)
        self.target1.debug = 'True'
        self.target2 = photo.Cleaning(self.TARGET_FILE_03)
        actual = self.target1.compare(self.target2.original, 80.0)
        self.target1.save(self.OUTPUT_DIR + os.sep + 'test_compare_true.jpg')
        self.assertTrue(actual)

    # 画像の類似度判定 似ていない
    def test_compare_false(self):
        self.target1 = photo.Cleaning(self.TARGET_FILE_03)
        self.target1.debug = 'True'
        self.target2 = photo.Cleaning(self.TARGET_FILE_04)
        actual = self.target1.compare(self.target2.original, 80.0)
        self.target1.save(self.OUTPUT_DIR + os.sep + 'test_compare_false.jpg')
        self.assertTrue(not actual)

    # 画像の類似度判定 判定結果取得
    def test_compare_get_status(self):
        self.target1 = photo.Cleaning(self.TARGET_FILE_03)
        self.target1.debug = 'True'
        self.target2 = photo.Cleaning(self.TARGET_FILE_03)
        self.target1.compare(self.target2.original, 80.0)
        self.target1.save(self.OUTPUT_DIR + os.sep + 'test_compare_true.jpg')
        actual = self.target1.compare_status
        self.assertTrue(actual)

    # モザイク例外(設定情報なし)
    def test_mosaic_setting_exception(self):
        expected = 'Failed to read the configuration file!'
        try:
            self.target = photo.Cleaning(self.TARGET_FILE_01)
            self.target._config.clear()
            self.target.mosaic()
        except exception.Photo_setting_exception as ex:
            actual = repr(ex)
            self.assertEqual(expected, actual)
        else:
            self.assertTrue(False)

    # モザイク例外(カスケードファイルなし)
    def test_mosaic_not_file_exception(self):
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
        compare_image = photo.Photo(self.TEST_FILE_DIR + os.sep + 'test_mosaic.jpg')
        self.target.compare(compare_image.image, 95.0)
        actual = self.target.compare_status
        self.assertTrue(actual)


if __name__ == '__main__':
    # unittestを実行
    unittest.main()
