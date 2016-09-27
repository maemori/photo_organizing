#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import unittest
import shutil

sys.path.append(os.pardir)
from photos import Photos
# import organize.exception as exception
import organize.util as util


class PhotoTest(unittest.TestCase):
    """Photo test class"""
    TEST_FILE_DIR = './resource/input_photo/set3'
    TEST_DIR = './photo'
    INPUT_DIR = TEST_DIR + os.sep + 'input'
    OUTPUT_DIR = TEST_DIR + os.sep + 'public'
    CASCADE_ORIGINAL_DIR = '../cascade'
    CASCADE_TEST_DIR = './cascade'
    TARGET_FILE_01 = INPUT_DIR + os.sep + '20160803_105354_000.jpg'
    TARGET_FILE_02 = INPUT_DIR + os.sep + '20160803_105458_000.jpg'
    TARGET_FILE_03 = INPUT_DIR + os.sep + '20160803_110935_000.jpg'
    TARGET_FILE_04 = INPUT_DIR + os.sep + '20160803_111247_000.jpg'

    # テスト初期化時に実行
    @classmethod
    def setUpClass(cls):
        try:
            # テスト用ディレクトリの設置
            if os.path.isfile(cls.INPUT_DIR):
                shutil.rmtree(cls.INPUT_DIR)
            shutil.copytree(cls.TEST_FILE_DIR, cls.INPUT_DIR)
            os.makedirs(cls.OUTPUT_DIR)
            os.makedirs(cls.CASCADE_TEST_DIR)
        except OSError:
            pass

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
        self.target = Photos()
        # カスケードファイルの設置
        cascade_func = util.files(util.copy, self.CASCADE_ORIGINAL_DIR)
        cascade_func(self.CASCADE_TEST_DIR)

    # テストメソッド後処理
    def tearDown(self):
        # カスケードファイルの削除
        cascade_func = util.files(util.delete, self.CASCADE_TEST_DIR)
        cascade_func()

    #
    def test_main_process(self):
        self.target.organize()
        self.assertTrue(True)


if __name__ == '__main__':
    # unittestを実行
    unittest.main()
