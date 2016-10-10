# -*- coding: utf-8 -*-
import os
import sys
import shutil
import unittest

sys.path.append(os.pardir)
from organize.main import main
import organize.cleaning as photo
import test_setting


class PhotoTest(unittest.TestCase):
    """Main processing test of."""
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
        self.setting = test_setting.Setting()

    def tearDown(self):
        """テストメソッド後処理"""
        # 設定の復元
        self.setting.config_file_set(os.path.join(
            self.setting.TEST_CONFIG_FILES_DIR, "config.ini"))
        self.setting.config_organize_file_set(os.path.join(
            self.setting.TEST_CONFIG_FILES_DIR, self.setting.TEST_ORGANIZE_CONFIG_DIR, "config.ini"))
        photo.Cleaning._CONFIG = {}
        photo.Cleaning.config()
        photo.Cleaning._CASCADE = {}
        photo.Cleaning.cascade()

    def test_main(self):
        """テスト：Main正常系"""
        expected = set(self.TEST_OUTPUT_FILES)
        # テストディレクトリ初期化
        self.setting.test_directory_initialization()
        # テスト用入力ファイルの設置
        shutil.copytree(self.TEST_FILE_DIR, os.path.join(self.setting.INPUT_DIR, self.TEST_DIR))
        # テストターゲットの実行
        main()
        # 作成された写真の確認
        actual = set(os.listdir(self.TEST_OUTPUT_DIR))
        # 部分集合で結果を確認
        compare = expected.issuperset(actual)
        self.assertTrue(compare)

    def test_main_exception_pass(self):
        """テスト：Main異常系"""
        # テストディレクトリ初期化
        self.setting.test_directory_initialization()
        # テスト用入力ファイルの設置
        shutil.copytree(self.TEST_FILE_DIR, os.path.join(self.setting.INPUT_DIR, self.TEST_DIR))
        # 空の設定ファイルを設置
        self.setting.config_file_set(os.path.join(
            self.setting.TEST_CONFIG_FILES_DIR, "config_ng_output_none.ini"))
        # 設定のクリア
        photo.Cleaning._CONFIG = {}
        # テストターゲットの実行
        main()
        # 出力先が空であることを確認
        result = False
        if not os.path.isdir(self.TEST_OUTPUT_DIR):
            result = True
        self.assertTrue(result)
