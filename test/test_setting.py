# -*- coding: utf-8 -*-
import os
import sys
import shutil

sys.path.append(os.pardir)
import everyone.util as util


class Setting:
    """Test Common Settings."""
    TEST_CONFIG_FILES_DIR = "./resource/test_conf"
    TEST_ORGANIZE_CONFIG_DIR = "organize"
    TEST_CONFIG_FILES = "config.ini"
    CONFIG_FILES_DIR = "./conf"
    CONFIG_ORGANIZE_FILES_DIR = os.path.join(CONFIG_FILES_DIR, TEST_ORGANIZE_CONFIG_DIR)
    TEST_DIR = "./photo"
    INPUT_DIR = os.path.join(TEST_DIR, "input")
    OUTPUT_DIR = os.path.join(TEST_DIR, "public")
    CASCADE_ORIGINAL_DIR = "../resource/cascade"
    CASCADE_TEST_DIR = "./resource/cascade"
    # テスト用設定ファイル
    _test_config_file = os.path.join(TEST_CONFIG_FILES_DIR, TEST_CONFIG_FILES)
    # 設定ファイル
    _config_file = os.path.join(CONFIG_FILES_DIR, TEST_CONFIG_FILES)
    # テスト用organize設定ファイル
    _test_organize_config = os.path.join(TEST_CONFIG_FILES_DIR, TEST_ORGANIZE_CONFIG_DIR, TEST_CONFIG_FILES)
    # organize設定ファイル
    _organize_config = os.path.join(CONFIG_FILES_DIR, TEST_ORGANIZE_CONFIG_DIR, TEST_CONFIG_FILES)

    def __init__(self):
        """初期化."""
        self.test_directory_initialization()

    def test_directory_initialization(self):
        """テストディレクトリ初期化."""
        # 設定ファイルの削除
        if os.path.isfile(self._config_file):
            os.remove(self._config_file)
        if os.path.isdir(self.CONFIG_ORGANIZE_FILES_DIR):
            shutil.rmtree(self.CONFIG_ORGANIZE_FILES_DIR)
        # テストディレクトリの削除
        if os.path.isdir(self.TEST_DIR):
            shutil.rmtree(self.TEST_DIR)
        # カスケードファイル格納ディレクリの削除
        if os.path.isdir(self.CASCADE_TEST_DIR):
            shutil.rmtree(self.CASCADE_TEST_DIR)
        # テスト用ディレクトリの作成
        os.makedirs(self.CONFIG_ORGANIZE_FILES_DIR)
        os.makedirs(self.TEST_DIR)
        os.makedirs(self.INPUT_DIR)
        os.makedirs(self.OUTPUT_DIR)
        os.makedirs(self.CASCADE_TEST_DIR)
        # テスト用設定の配置
        shutil.copy(self._test_config_file, self._config_file)
        shutil.copy(self._test_organize_config, self._organize_config)
        # カスケードファイルの設置
        cascade_func = util.files(util.copy, self.CASCADE_ORIGINAL_DIR)
        cascade_func(self.CASCADE_TEST_DIR)

    def config_file_set(self, filename: str):
        """指定されたファイルで設定ファイルを置き換え."""
        if os.path.isfile(self._config_file):
            os.remove(self._config_file)
        shutil.copy(filename, self._config_file)

    def config_organize_file_set(self, filename: str):
        """指定されたファイルで設organize設定ファイルを置き換え."""
        if os.path.isfile(self._organize_config):
            os.remove(self._organize_config)
        shutil.copy(filename, self._organize_config)
