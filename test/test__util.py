#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import shutil
import sys
import unittest

sys.path.append(os.pardir)
import everyone.util as util

import test_setting


class PhotoTest(unittest.TestCase):
    """Photo test class"""
    setting = test_setting.Setting()
    TEST_FILE_DIR_01 = './resource/test_input_photo/set1'
    TEST_FILE_DIR_02 = './resource/test_input_photo/set4'

    # テスト初期化時に実行
    @classmethod
    def setUpClass(cls):
        pass

    # テスト終了時に実行
    @classmethod
    def tearDownClass(cls):
        pass

    # テストメソッド前処理
    def setUp(self):
        pass

    # テストメソッド後処理
    def tearDown(self):
        if os.path.isdir(self.setting.TEST_DIR):
            shutil.rmtree(self.setting.TEST_DIR)

    # ファイルコピーのテスト
    def test_files_copy(self):
        expected = 7
        # テストターゲットの実行
        copy_func = util.files(util.copy, self.TEST_FILE_DIR_01)
        actual = copy_func(self.setting.INPUT_DIR)
        self.assertEqual(expected, len(actual))

    # ファイル削除のテスト
    def test_files_delete(self):
        expected = 7
        copy_func = util.files(util.copy, self.TEST_FILE_DIR_01)
        copy_func(self.setting.INPUT_DIR)
        # テストターゲットの実行
        delete_func = util.files(util.delete, self.setting.INPUT_DIR)
        actual = delete_func()
        self.assertEqual(expected, len(actual))

    # 日付ディレクトリの作成テスト
    def test_make_directory(self):
        expected = "./photo/input/2016/01/2016-01-02"
        # テストターゲットの実行
        actual = util.make_directory(self.setting.INPUT_DIR, "2016-01-02")
        self.assertEqual(expected, actual)

    # 入力ディクリ処理後削除処理のテスト
    def test_input_directory_delete(self):
        os.makedirs("./photo/input/2016/08/04/meta")
        # テストターゲットの実行
        util.delete_directory(self.setting.INPUT_DIR)
        if not os.path.isdir(self.setting.INPUT_DIR):
            self.assertTrue(True)
        else:
            self.assertTrue(False)

if __name__ == '__main__':
    # unittestを実行
    unittest.main()
