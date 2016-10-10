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
    """Of utility class test."""
    setting = test_setting.Setting()
    TEST_FILE_DIR_01 = "./resource/test_input_photo/set1"

    @classmethod
    def setUpClass(cls):
        """テスト初期化時に実行"""
        pass

    @classmethod
    def tearDownClass(cls):
        """テスト終了時に実行"""
        pass

    def setUp(self):
        """テストメソッド前処理"""
        pass

    def tearDown(self):
        """テストメソッド後処理"""
        if os.path.isdir(self.setting.TEST_DIR):
            shutil.rmtree(self.setting.TEST_DIR)

    def test_files_copy(self):
        """テスト：ファイルコピーのテスト"""
        expected = 7
        # テストターゲットの実行
        copy_func = util.files(util.copy, self.TEST_FILE_DIR_01)
        actual = copy_func(self.setting.INPUT_DIR)
        self.assertEqual(expected, len(actual))

    def test_files_delete(self):
        """テスト：ファイル削除のテスト"""
        expected = 7
        copy_func = util.files(util.copy, self.TEST_FILE_DIR_01)
        copy_func(self.setting.INPUT_DIR)
        # テストターゲットの実行
        delete_func = util.files(util.delete, self.setting.INPUT_DIR)
        actual = delete_func()
        self.assertEqual(expected, len(actual))

    def test_make_directory(self):
        """テスト：日付ディレクトリの作成テスト"""
        expected = "./photo/input/2016/01/2016-01-02"
        # テストターゲットの実行
        actual = util.make_directory(self.setting.INPUT_DIR, "2016-01-02")
        self.assertEqual(expected, actual)

    def test_input_directory_delete(self):
        """テスト：入力ディクリ処理後削除処理のテスト"""
        os.makedirs("./photo/input/2016/08/04/meta")
        result = False
        # テストターゲットの実行
        util.delete_directory(self.setting.INPUT_DIR)
        if not os.path.isdir(self.setting.INPUT_DIR):
            result = True
        self.assertTrue(result)
