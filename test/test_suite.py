#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

import test.test_photo as photo
import test.test_cleaning as cleaning
import test.test_photos as photos


# テストスイートを作成して返却します
def suite():
    # テストスイートを定義します
    test_suite = unittest.TestSuite()
    # addTestを用いてテストスイートに追加していきます
    test_suite.addTest(unittest.makeSuite(photo.PhotoTest))
    test_suite.addTest(unittest.makeSuite(cleaning.PhotoTest))
    test_suite.addTest(unittest.makeSuite(photos.PhotoTest))
    return test_suite

if __name__ == "__main__":
    # 作成したテストスイートを呼び出して、TextTestRunnerで実行します
    mySuite = suite()
    unittest.TextTestRunner().run(mySuite)
