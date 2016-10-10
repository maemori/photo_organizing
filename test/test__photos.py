# -*- coding: utf-8 -*-
import os
import sys
import shutil
import unittest

sys.path.append(os.pardir)
import organize.cleaning as photo
from photos import Photos
import organize.exception as exception
import test_setting


class PhotoTest(unittest.TestCase):
    """Test of photo organizing class."""
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

    def test_config_none(self):
        """テスト：設定ファイルなし"""
        expected = "Failed to read the configuration file!"
        try:
            # テストディレクトリ初期化
            self.setting.test_directory_initialization()
            # テスト用入力ファイルの設置
            shutil.copytree(self.TEST_FILE_DIR, os.path.join(self.setting.INPUT_DIR, self.TEST_DIR))
            # からの設定ファイルを設置
            self.setting.config_file_set(os.path.join(
                self.setting.TEST_CONFIG_FILES_DIR, "config_ng_none.ini"))
            photo.Cleaning.config()
            # オブジェクトの生成
            Photos()
        except exception.Photo_setting_exception as ex:
            actual = repr(ex)
            self.assertEqual(expected, actual)

    def test_move_files_func_exception(self):
        """テスト：指定ファイル移動処理例外"""
        expected = "Photo organizing exception!"
        try:
            # オブジェクトの生成
            target = Photos()
            target._move_files_func("./test/test_delete_unneeded_func_exception.mp4")
        except exception.Photo_exception as ex:
            actual = repr(ex)
            self.assertEqual(expected, actual)

    def test_delete_unneeded_func_exception(self):
        """テスト：指定ファイル削除処理例外"""
        expected = "Photo organizing exception!"
        try:
            # オブジェクトの生成
            target = Photos()
            target._delete_unneeded_func("./test/test_delete_unneeded_func_exception.json")
        except exception.Photo_exception as ex:
            actual = repr(ex)
            self.assertEqual(expected, actual)

    def test_input_dir_none(self):
        """テスト：設定ファイル・入力ディレクトリ指定なし"""
        # テストディレクトリ初期化
        self.setting.test_directory_initialization()
        # テスト用入力ファイルの設置
        shutil.copytree(self.TEST_FILE_DIR, os.path.join(self.setting.INPUT_DIR, self.TEST_DIR))
        # テスト用の設定ファイルを設置
        self.setting.config_file_set(os.path.join(
            self.setting.TEST_CONFIG_FILES_DIR, "config_ng_input_none.ini"))
        # 設定のクリア
        photo.Cleaning._CONFIG = {}
        # オブジェクトの生成
        target = Photos()
        # テストターゲットの実行
        target.organize()
        # 出力先が空であることを確認
        result = False
        if not os.path.isdir(self.TEST_OUTPUT_DIR):
            result = True
        self.assertTrue(result)

    def test_output_dir_none(self):
        """テスト：設定ファイル・出力ディレクトリ指定なし"""
        expected = "Photo organizing exception!"
        try:
            # テストディレクトリ初期化
            self.setting.test_directory_initialization()
            # テスト用入力ファイルの設置
            shutil.copytree(self.TEST_FILE_DIR, os.path.join(self.setting.INPUT_DIR, self.TEST_DIR))
            # テスト用の設定ファイルを設置
            self.setting.config_file_set(os.path.join(
                self.setting.TEST_CONFIG_FILES_DIR, "config_ng_output_none.ini"))
            # 設定のクリア
            photo.Cleaning._CONFIG = {}
            # オブジェクトの生成
            target = Photos()
            # テストターゲットの実行
            target.organize()
        except exception.Photo_exception as ex:
            actual = repr(ex)
            self.assertEqual(expected, actual)

    def test_organize_func_exception(self):
        """テスト：写真整理処理例外（設定値なし）"""
        expected = "Failed to read the configuration file!"
        try:
            # テストディレクトリ初期化
            self.setting.test_directory_initialization()
            # テスト用入力ファイルの設置
            shutil.copytree(self.TEST_FILE_DIR, os.path.join(self.setting.INPUT_DIR, self.TEST_DIR))
            # 空の設定ファイルを設置
            self.setting.config_organize_file_set(os.path.join(
                self.setting.TEST_CONFIG_FILES_DIR, self.setting.TEST_ORGANIZE_CONFIG_DIR, "config_ng_none.ini"))
            # 設定のクリア
            photo.Cleaning._CONFIG = {}
            photo.Cleaning._CASCADE = {}
            # オブジェクトの生成
            target = Photos()
            # テストターゲットの実行
            target.organize()
        except exception.Photo_setting_exception as ex:
            actual = repr(ex)
            self.assertEqual(expected, actual)

    def test_organize_func_mosaic_value_exception(self):
        """テスト：写真整理処理例外(カスケード設置値異常)"""
        expected = "Fail to recognize the face!"
        try:
            # テストディレクトリ初期化
            self.setting.test_directory_initialization()
            # テスト用入力ファイルの設置
            shutil.copytree(self.TEST_FILE_DIR, os.path.join(self.setting.INPUT_DIR, self.TEST_DIR))
            # 値が不正なの設定ファイルを設置
            self.setting.config_organize_file_set(os.path.join(
                self.setting.TEST_CONFIG_FILES_DIR, self.setting.TEST_ORGANIZE_CONFIG_DIR, "config_ng_val.ini"))
            # 設定のクリア
            photo.Cleaning._CONFIG = {}
            photo.Cleaning._CASCADE = {}
            # オブジェクトの生成
            target = Photos()
            # テストターゲットの実行
            target.organize()
        except exception.Photo_cascade_exception as ex:
            actual = repr(ex)
            self.assertEqual(expected, actual)

    def test_thumbnail_exception(self):
        """テスト：サムネイル処理例外"""
        expected = "It failed to create a thumbnail image!"
        try:
            # テストディレクトリ初期化
            self.setting.test_directory_initialization()
            # テスト用入力ファイルの設置
            shutil.copytree(self.TEST_FILE_DIR, os.path.join(self.setting.INPUT_DIR, self.TEST_DIR))
            # 空の設定ファイルを設置
            self.setting.config_file_set(os.path.join(
                self.setting.TEST_CONFIG_FILES_DIR, "config_ng_thumbnail_exception.ini"))
            # オブジェクトの生成
            target = Photos()
            # テストターゲットの実行
            target.organize()
        except exception.Photo_thumbnail_exception as ex:
            actual = repr(ex)
            self.assertEqual(expected, actual)

    def test_base_flow(self):
        """テスト：基本フローのテスト"""
        expected = set(self.TEST_OUTPUT_FILES)
        # テストディレクトリ初期化
        self.setting.test_directory_initialization()
        # テスト用入力ファイルの設置
        shutil.copytree(self.TEST_FILE_DIR, os.path.join(self.setting.INPUT_DIR, self.TEST_DIR))
        # オブジェクトの生成
        target = Photos()
        # テストターゲットの実行
        target.organize()
        # 作成された写真の確認
        actual = set(os.listdir(self.TEST_OUTPUT_DIR))
        # 部分集合で結果を確認
        compare = expected.issuperset(actual)
        self.assertTrue(compare)

    def test_base_flow_mosaic_off(self):
        """テスト：基本フローのテスト（モザイク指定なし）"""
        expected = set(self.TEST_OUTPUT_FILES)
        # テストディレクトリ初期化
        self.setting.test_directory_initialization()
        # テスト用入力ファイルの設置
        shutil.copytree(self.TEST_FILE_DIR, os.path.join(self.setting.INPUT_DIR, self.TEST_DIR))
        # テスト用の設定ファイルを設置
        self.setting.config_file_set(os.path.join(
            self.setting.TEST_CONFIG_FILES_DIR, "config_mosaic_off.ini"))
        # オブジェクトの生成
        target = Photos()
        # テストターゲットの実行
        target.organize()
        # 作成された写真の確認
        actual = set(os.listdir(self.TEST_OUTPUT_DIR))
        # 部分集合で結果を確認
        compare = expected.issuperset(actual)
        self.assertTrue(compare)

    def test_base_flow_thumbnail(self):
        """テスト：基本フローのテスト（サムネイル２段出力）"""
        expected = set(self.TEST_OUTPUT_FILES)
        # テストディレクトリ初期化
        self.setting.test_directory_initialization()
        # テスト用入力ファイルの設置
        shutil.copytree(self.TEST_FILE_DIR, os.path.join(self.setting.INPUT_DIR, self.TEST_DIR))
        # テスト用の設定ファイルを設置
        self.setting.config_file_set(os.path.join(
            self.setting.TEST_CONFIG_FILES_DIR, "config_thumbnail.ini"))
        # オブジェクトの生成
        target = Photos()
        # テストターゲットの実行
        target.organize()
        # 作成された写真の確認
        actual = set(os.listdir(self.TEST_OUTPUT_DIR))
        # 部分集合で結果を確認
        compare = expected.issuperset(actual)
        self.assertTrue(compare)

    def test_base_flow_backup_dir_none(self):
        """テスト：設定ファイル・バックアップディレクトリ指定なし"""
        expected = set(self.TEST_OUTPUT_FILES)
        # テストディレクトリ初期化
        self.setting.test_directory_initialization()
        # テスト用入力ファイルの設置
        shutil.copytree(self.TEST_FILE_DIR, os.path.join(self.setting.INPUT_DIR, self.TEST_DIR))
        # テスト用の設定ファイルを設置
        self.setting.config_file_set(os.path.join(
            self.setting.TEST_CONFIG_FILES_DIR, "config_backup_none.ini"))
        # 設定のクリア
        photo.Cleaning._CONFIG = {}
        # オブジェクトの生成
        target = Photos()
        # テストターゲットの実行
        target.organize()
        # ターゲットのディクトリが空であること
        result = False
        if not os.path.isdir("./photo/backup"):
            result = True
        # 作成された写真の確認
        actual = set(os.listdir(self.TEST_OUTPUT_DIR))
        # 部分集合で結果を確認
        compare = expected.issuperset(actual)
        self.assertTrue(compare and result)

    def test_base_flow_trash_dir_none(self):
        """テスト：設定ファイル・破棄ディレクトリ指定なし"""
        expected = set(self.TEST_OUTPUT_FILES)
        # テストディレクトリ初期化
        self.setting.test_directory_initialization()
        # テスト用入力ファイルの設置
        shutil.copytree(self.TEST_FILE_DIR, os.path.join(self.setting.INPUT_DIR, self.TEST_DIR))
        # テスト用の設定ファイルを設置
        self.setting.config_file_set(os.path.join(
            self.setting.TEST_CONFIG_FILES_DIR, "config_trash_none.ini"))
        # オブジェクトの生成
        target = Photos()
        # テストターゲットの実行
        target.organize()
        # ターゲットのディクトリが空であること
        result = False
        if not os.path.isdir("./photo/trash"):
            result = True
        # 作成された写真の確認
        actual = set(os.listdir(self.TEST_OUTPUT_DIR))
        # 部分集合で結果を確認
        compare = expected.issuperset(actual)
        self.assertTrue(compare and result)

    def test_base_flow_backup_trash_dir_none(self):
        """テスト：設定ファイル・バックアップ&破棄ディレクトリ指定なし"""
        expected = set(self.TEST_OUTPUT_FILES)
        # テストディレクトリ初期化
        self.setting.test_directory_initialization()
        # テスト用入力ファイルの設置
        shutil.copytree(self.TEST_FILE_DIR, os.path.join(self.setting.INPUT_DIR, self.TEST_DIR))
        # テスト用の設定ファイルを設置
        self.setting.config_file_set(os.path.join(
            self.setting.TEST_CONFIG_FILES_DIR, "config_backup_trash_none.ini"))
        # オブジェクトの生成
        target = Photos()
        # テストターゲットの実行
        target.organize()
        # ターゲットのディクトリが空であること
        result_backup = False
        if not os.path.isdir("./photo/backup"):
            result_backup = True
        result_trash = False
        if not os.path.isdir("./photo/trash"):
            result_trash = True
        # 作成された写真の確認
        actual = set(os.listdir(self.TEST_OUTPUT_DIR))
        # 部分集合で結果を確認
        compare = expected.issuperset(actual)
        self.assertTrue(compare and result_backup and result_trash)
