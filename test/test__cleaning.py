# -*- coding: utf-8 -*-
import os
import sys
import unittest

sys.path.append(os.pardir)
import organize.cleaning as photo
import organize.exception as exception
import everyone.util as util
import test_setting


class PhotoTest(unittest.TestCase):
    """Cleaning class test."""
    setting = test_setting.Setting()
    TEST_FILE_DIR = "./resource/test_input_photo/set2"
    TARGET_FILE_01 = os.path.join(setting.INPUT_DIR, "20160803_105354_000.jpg")
    TARGET_FILE_02 = os.path.join(setting.INPUT_DIR, "20160803_105458_000.jpg")
    TARGET_FILE_03 = os.path.join(setting.INPUT_DIR, "20160803_110935_000.jpg")
    TARGET_FILE_04 = os.path.join(setting.INPUT_DIR, "20160803_111247_000.jpg")

    @classmethod
    def setUpClass(cls):
        """テスト初期化時に実行."""
        # テスト用入力ファイルの設置
        copy_func = util.files(util.copy, cls.TEST_FILE_DIR)
        copy_func(cls.setting.INPUT_DIR)

    @classmethod
    def tearDownClass(cls):
        """テスト終了時に実行."""
        pass

    def setUp(self):
        """テストメソッド前処理."""
        pass

    def tearDown(self):
        """テストメソッド後処理."""
        # 設定の復元
        self.setting.config_file_set(os.path.join(
            self.setting.TEST_CONFIG_FILES_DIR, "config.ini"))
        self.setting.config_organize_file_set(os.path.join(
            self.setting.TEST_CONFIG_FILES_DIR, self.setting.TEST_ORGANIZE_CONFIG_DIR, "config.ini"))
        photo.Cleaning._CONFIG = {}
        photo.Cleaning.config()
        photo.Cleaning._CASCADE = {}
        photo.Cleaning.cascade()

    def test_out_of_focus_true(self):
        """テスト：ピンボケ判定 -> ピンボケ."""
        # オブジェクトの生成
        target = photo.Cleaning(self.TARGET_FILE_01)
        # テストターゲットの実行
        actual = target.out_of_focus(30.0)
        target.save(os.path.join(self.setting.OUTPUT_DIR, "test_out_of_focus_true.jpg"))
        self.assertTrue(actual)

    def test_out_of_focus_false(self):
        """テスト：ピンボケ判定 -> ピンボケ."""
        # オブジェクトの生成
        target = photo.Cleaning(self.TARGET_FILE_02)
        # テストターゲットの実行
        actual = target.out_of_focus(30.0)
        target.save(os.path.join(self.setting.OUTPUT_DIR, "test_out_of_focus_false.jpg"))
        self.assertTrue(not actual)

    def test_out_of_focus_get_status(self):
        """テスト：ピンボケ判定 -> 判定結果取得."""
        target = photo.Cleaning(self.TARGET_FILE_01)
        # テストターゲットの実行
        target.out_of_focus(30.0)
        actual = target.blurry_status
        target.save(os.path.join(self.setting.OUTPUT_DIR, "test_out_of_focus_true.jpg"))
        self.assertTrue(actual)

    def test_compare_true(self):
        """テスト：画像の類似度判定 似ている."""
        target1 = photo.Cleaning(self.TARGET_FILE_03)
        target2 = photo.Cleaning(self.TARGET_FILE_03)
        # テストターゲットの実行
        actual = target1.compare(target2.original, 80.0)
        target1.save(os.path.join(self.setting.OUTPUT_DIR, "test_compare_true.jpg"))
        self.assertTrue(actual)

    def test_compare_false(self):
        """テスト：画像の類似度判定 似ていない"""
        # オブジェクトの生成
        target1 = photo.Cleaning(self.TARGET_FILE_03)
        # オブジェクトの生成
        target2 = photo.Cleaning(self.TARGET_FILE_04)
        # テストターゲットの実行
        actual = target1.compare(target2.original, 80.0)
        target1.save(os.path.join(self.setting.OUTPUT_DIR, "test_compare_false.jpg"))
        self.assertTrue(not actual)

    def test_compare_get_status(self):
        """テスト：画像の類似度判定 判定結果取得."""
        # オブジェクトの生成
        target1 = photo.Cleaning(self.TARGET_FILE_03)
        # オブジェクトの生成
        target2 = photo.Cleaning(self.TARGET_FILE_03)
        # テストターゲットの実行
        target1.compare(target2.original, 80.0)
        target1.save(os.path.join(self.setting.OUTPUT_DIR, "test_compare_true.jpg"))
        actual = target1.compare_status
        self.assertTrue(actual)

    def test_mosaic(self):
        """テスト：モザイク."""
        # オブジェクトの生成
        target = photo.Cleaning(self.TARGET_FILE_01)
        target.mosaic()
        output_file = os.path.join(self.setting.OUTPUT_DIR, "test_mosaic.jpg")
        target.save(output_file)
        compare_image = photo.Photo(os.path.join(self.TEST_FILE_DIR, "test_mosaic.jpg"))
        # テストターゲットの実行
        target.compare(compare_image.image, 95.0)
        actual = target.compare_status
        self.assertTrue(actual)

    def test_mosaic_debug(self):
        """テスト：モザイク・デバッグモード."""
        # オブジェクトの生成
        target = photo.Cleaning(self.TARGET_FILE_01)
        target.debug = "True"
        target.mosaic()
        output_file = os.path.join(self.setting.OUTPUT_DIR, "test_mosaic.jpg")
        target.save(output_file)
        compare_image = photo.Photo(os.path.join(self.TEST_FILE_DIR, "test_mosaic.jpg"))
        # テストターゲットの実行
        target.compare(compare_image.image, 95.0)
        actual = target.compare_status
        self.assertTrue(actual)

    def test_config_delete(self):
        """テスト：設定ファイルなし(./conf/organize/config.ini)."""
        expected = "Failed to read the configuration file!"
        # 設定ファイルの削除
        os.remove(os.path.join(self.setting.CONFIG_FILES_DIR, self.setting.TEST_CONFIG_FILES))
        try:
            # オブジェクトの生成
            target = photo.Cleaning(self.TARGET_FILE_01)
            # 設定のクリア
            photo.Cleaning._CONFIG = {}
            # テストターゲットの実行
            target.mosaic()
        except exception.Photo_setting_exception as ex:
            actual = repr(ex)
            self.assertEqual(expected, actual)

    def test_config_none(self):
        """テスト：設定なし(./conf/organize/config.ini)."""
        expected = "Failed to read the configuration file!"
        try:
            # 空の設定ファイルを設置
            self.setting.config_organize_file_set(os.path.join(
                self.setting.TEST_CONFIG_FILES_DIR, self.setting.TEST_ORGANIZE_CONFIG_DIR, "config_ng_none.ini"))
            # オブジェクトの生成
            photo.Cleaning(self.TARGET_FILE_01)
            # 設定のクリア
            photo.Cleaning._CONFIG = {}
            # 設定の読み込み
            photo.Cleaning.config()
        except exception.Photo_setting_exception as ex:
            actual = repr(ex)
            self.assertEqual(expected, actual)

    def test_mosaic_setting_exception(self):
        """テスト：モザイク例外(設定情報なし)."""
        expected = "Failed to read the configuration file!"
        try:
            # オブジェクトの生成
            target = photo.Cleaning(self.TARGET_FILE_01)
            photo.Cleaning._CONFIG = {}
            # テストターゲットの実行
            target.mosaic()
        except exception.Photo_setting_exception as ex:
            actual = repr(ex)
            self.assertEqual(expected, actual)

    def test_mosaic_not_setting_exception(self):
        """テスト：モザイク例外(カスケード設定なし)."""
        expected = "Failed to read the configuration file!"
        try:
            # オブジェクトの生成
            target = photo.Cleaning(self.TARGET_FILE_01)
            # 空の設定ファイルを設置
            self.setting.config_organize_file_set(os.path.join(
                self.setting.TEST_CONFIG_FILES_DIR, self.setting.TEST_ORGANIZE_CONFIG_DIR, "config_ng_none.ini"))
            # カスケード設定のクリア
            photo.Cleaning._CONFIG = {}
            photo.Cleaning._CASCADE = {}
            # 設定の読み込み
            target.cascade()
        except exception.Photo_setting_exception as ex:
            actual = repr(ex)
            self.assertEqual(expected, actual)

    def test_mosaic_not_file_exception(self):
        """テスト：モザイク例外(カスケードファイルなし)."""
        expected = "Fail to recognize the face!"
        try:
            # オブジェクトの生成
            target = photo.Cleaning(self.TARGET_FILE_01)
            # 空の設定ファイルを設置
            self.setting.config_organize_file_set(os.path.join(
                self.setting.TEST_CONFIG_FILES_DIR, self.setting.TEST_ORGANIZE_CONFIG_DIR, "config_ng_file.ini"))
            # カスケード設定のクリア
            photo.Cleaning._CONFIG = {}
            photo.Cleaning._CASCADE = {}
            # 設定の読み込み
            target.config()
            target.cascade()
            # テストターゲットの実行
            target.mosaic()
        except exception.Photo_cascade_exception as ex:
            actual = repr(ex)
            self.assertEqual(expected, actual)

    def test_mosaic_value_exception(self):
        """テスト：モザイク例外(カスケード設置値異常)."""
        expected = "Fail to recognize the face!"
        try:
            # オブジェクトの生成
            target = photo.Cleaning(self.TARGET_FILE_01)
            # 値が不正なの設定ファイルを設置
            self.setting.config_organize_file_set(os.path.join(
                self.setting.TEST_CONFIG_FILES_DIR, self.setting.TEST_ORGANIZE_CONFIG_DIR, "config_ng_val.ini"))
            # カスケード設定のクリア
            photo.Cleaning._CONFIG = {}
            photo.Cleaning._CASCADE = {}
            # 設定の読み込み
            target.config()
            target.cascade()
            # テストターゲットの実行
            target.mosaic()
        except exception.Photo_cascade_exception as ex:
            actual = repr(ex)
            self.assertEqual(expected, actual)
