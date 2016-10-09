#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import shutil
import unittest

sys.path.append(os.pardir)
from photos import Photos
import organize.exception as exception

import test_setting


class PhotoTest(unittest.TestCase):
    """Photo test class"""
    setting = test_setting.Setting()
    TEST_FILE_DIR = "./resource/test_input_photo/set3"
    TEST_DIR = "test"
    TEST_OUTPUT_DIR = "./photo/public/2016/08/2016-08-04"
    TEST_OUTPUT_FILES = [
        "20160804_021113_000.mp4",
        "20160804_060848_000.jpg",
        "20160804_060920_000.jpg",
        "20160804_064317_000.jpg",
        "20160804_064349_000.jpg",
        "20160804_065149_000.jpg",
        "20160804_065221_000.jpg",
        "20160804_090506_000.jpg",
        "20160804_090538_000.jpg",
        "20160804_090610_000.jpg",
        "thumbnail.png"]

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
        pass

    # 写真整理処理例外
    def test_organize_func_exception(self):
        pass

    # サムネイル処理例外
    def test_thumbnail_exception(self):
        pass

    # ファイル移動処理例外
    def test_move_files_func_exception(self):
        pass

    # ファイル削除処理例外
    def test_delete_unneeded_func_exception(self):
        pass

    # 基本フローのテスト
    def test_base_flow(self):
        try:
            expected = self.TEST_OUTPUT_FILES
            # テストディレクトリ初期化
            self.setting.test_directory_initialization()
            # テスト用入力ファイルの設置
            shutil.copytree(self.TEST_FILE_DIR, os.path.join(self.setting.INPUT_DIR, self.TEST_DIR))
            # オブジェクトの生成
            target = Photos()
            # テストターゲットの実行
            target.organize()
            # 作成された写真の確認
            actual = os.listdir(self.TEST_OUTPUT_DIR)
            compare = (expected.sort() == actual.sort())
            self.assertTrue(compare)
        except exception.Photo_exception:
            self.assertTrue(False)

    # 基本フローのテスト（モザイク指定なし）
    def test_base_flow_mosaic_off(self):
        try:
            expected = self.TEST_OUTPUT_FILES
            # テストディレクトリ初期化
            self.setting.test_directory_initialization()
            # テスト用入力ファイルの設置
            shutil.copytree(self.TEST_FILE_DIR, os.path.join(self.setting.INPUT_DIR, self.TEST_DIR))
            # 空の設定ファイルを設置
            self.setting.config_file_set(os.path.join(
                self.setting.TEST_CONFIG_FILES_DIR, "config_mosaic_off.ini"))
            # オブジェクトの生成
            target = Photos()
            # テストターゲットの実行
            target.organize()
            # 作成された写真の確認
            actual = os.listdir(self.TEST_OUTPUT_DIR)
            compare = (expected.sort() == actual.sort())
            self.assertTrue(compare)
        except exception.Photo_exception:
            self.assertTrue(False)
        finally:
            # 設定ファイルの復元
            self.setting.config_file_set(os.path.join(
                self.setting.TEST_CONFIG_FILES_DIR, "config.ini"))

if __name__ == '__main__':
    # unittestを実行
    unittest.main()
