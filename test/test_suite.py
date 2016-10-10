#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

import test.test__photo as photo
import test.test__cleaning as cleaning
import test.test__util as util
import test.test__photos as photos
import test.test__main as main
import test_setting


def suite():
    """テストスイートの作成"""
    test_suite = unittest.TestSuite()
    # 写真基底クラスのテスト
    test_suite.addTest(unittest.makeSuite(photo.PhotoTest))
    # 写真の整理を行うクラスのテスト (クラス変数を削除するテストが含めれているため最後に追加)
    test_suite.addTest(unittest.makeSuite(cleaning.PhotoTest))
    # ユーティリティのテスト
    test_suite.addTest(unittest.makeSuite(util.PhotoTest))
    # 複数の写真をまとめて整理するクラスのテスト
    test_suite.addTest(unittest.makeSuite(photos.PhotoTest))
    # メインのテスト
    test_suite.addTest(unittest.makeSuite(main.PhotoTest))
    return test_suite

if __name__ == "__main__":
    """テストスイートの実行"""
    mySuite = suite()
    unittest.TextTestRunner().run(mySuite)
    # テストディレクトリ初期化
    setting = test_setting.Setting()
    setting.test_directory_initialization()
