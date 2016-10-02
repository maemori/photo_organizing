#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

import test.test_photo as photo
import test.test_cleaning as cleaning
import test.test_photos as photos


def suite():
    """テストスイートの作成"""
    test_suite = unittest.TestSuite()
    # addTestを用いてテストスイートに追加
    # 複数の写真をまとめて整理するクラスのテスト
    test_suite.addTest(unittest.makeSuite(photos.PhotoTest))
    # 写真基底クラスのテスト
    test_suite.addTest(unittest.makeSuite(photo.PhotoTest))
    # 写真の整理を行うクラスのテスト (クラス変数を削除するテストが含めれているため最後に追加)
    test_suite.addTest(unittest.makeSuite(cleaning.PhotoTest))
    return test_suite

if __name__ == "__main__":
    """テストスイートの実行"""
    mySuite = suite()
    unittest.TextTestRunner().run(mySuite)
