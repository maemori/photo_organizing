# -*- coding: utf-8 -*-
""" garbage
ライフログとして撮影された大量の写真を整理する役割を持ったクラスです。
機能は写真のピンボケ判定、連続で作成された写真の類似度を判定します。
また、顔を認識しモザイク化を行います。
"""
from photo.photo import Photo

import os
import configparser

import cv2


class Cleaning(Photo):
    """Garbage 写真の整理を行うクラス
        機能
        ・写真のピンボケ判定
        ・同じような写真の判別
        ・顔のモザイク
    """
    def __init__(self, filename):
        super().__init__(filename)
        # 設定
        self._config = configparser.ConfigParser()
        self._config.read("photo" + os.sep + "config.ini")
        # 初期設置
        self._compare_status = False
        self._blurry_status = None

    def __getattr__(self, item):
        try:
            super().__getattr__(item)
        except AttributeError:
            if item == 'compare_status':
                return self._compare_status
            elif item == 'blurry_status':
                return self._blurry_status
            else:
                raise AttributeError(item)

    def out_of_focus(self, blurry_value):
        """
        ピンボケ判定
            ボケ具合閾値をパーセント指定し画像のボケ具合を判定
            100%は一眼レフなどシビアな判定結果、65%ぐらいが低スペックなカメラに合う

        :param blurry_value: ボケ具合閾値
        :return:
        """
        try:
            # エッジ検出
            focus = cv2.Laplacian(self._gray, cv2.CV_64F).var()
            # ピンボケ判定
            if focus < float(blurry_value):
                # ボケている
                self._blurry_status = False
            else:
                # くっきり
                self._blurry_status = True
            # Debug
            if self._debug:
                if self._blurry_status:
                    text_blurry = "Clearly"
                    color = (238, 110, 64)
                else:
                    text_blurry = "Blurry"
                    color = (84, 76, 148)
                print("- {}: {:.2f}".format(text_blurry, focus))
                cv2.putText(self._image, "{}: {:.2f}".format(text_blurry, focus), (50, self.debug_text_y()),
                            cv2.FONT_HERSHEY_SIMPLEX, 2.0, color, 3)
            return self._blurry_status
        except:
            raise

    def compare(self, image, compare_value):
        """
        オリジナル画像と入力画像の類似度判定する
        :param compare_value:
        :param image:
        :return:
        """
        try:
            # 類似判定
            compare_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            # ヒストグラム取得
            this_histogram = cv2.calcHist(self._gray, [0], None, [256], [0, 256])
            compare_histogram = cv2.calcHist(compare_image, [0], None, [256], [0, 256])
            # 類似度
            total = 0
            for i in range(len(this_histogram)):
                total += min(this_histogram[i], compare_histogram[i])
            difference = float(total) / sum(this_histogram)
            if difference >= (float(compare_value) / 100):
                # 似ている
                self._compare_status = False
            else:
                # 似ていない
                self._compare_status = True
            # Debug
            if self._debug:
                color = (238, 110, 64)
                print("- {}: {:.2f}%".format("Compare: ", float(difference) * 100))
                cv2.putText(self._image, "{}: {:.2f}%".format("Compare: ", float(difference) * 100),
                            (50, self.debug_text_y()), cv2.FONT_HERSHEY_SIMPLEX, 2.0, color, 3)
        finally:
            return self._compare_status

    def mosaic(self):
        """
        モザイク
        設定ファイル(config.ini)の[cascade_file]セクションに定義されているカスケードファイルを読み込みに画像から該当する対象に
        モザイクを適用する。カスケードファイルは[cascade_file]に定義されている全てが適用される

        :return:

        """
        try:
            for key in self._config['cascade_file']:
                file = self._config['cascade_file'][key]
                face = self.__cascade(file)
                if self._debug:
                    color = (238, 110, 64)
                    print("- {}: {:5d}".format(key, face))
                    cv2.putText(self._image, "{}: {:d}".format(key, face), (50, self.debug_text_y()),
                                cv2.FONT_HERSHEY_SIMPLEX, 2.0, color, 3)
        except:
            raise

    def __cascade(self, cascade_file):
        """
        顔認識

        :param cascade_file: カスケードファイル
        :return: 顔の検出数
        """
        try:
            # 顔探索用のカスケード型分類器を取得
            cascade = cv2.CascadeClassifier(cascade_file)
            """
            物体認識（顔認識）の実行
                image – CV_8U 型の行列．ここに格納されている画像中から物体が検出されます
                objects – 矩形を要素とするベクトル．それぞれの矩形は，検出した物体を含みます
                scaleFactor – 各画像スケールにおける縮小量を表します
                minNeighbors – 物体候補となる矩形は，最低でもこの数だけの近傍矩形を含む必要があります
                flags – このパラメータは，新しいカスケードでは利用されません．古いカスケードに対しては，cvHaarDetectObjects 関数の場合と同じ意味を持ちます
                minSize – 物体が取り得る最小サイズ．これよりも小さい物体は無視されます
            """
            # カスケード分類器で横顔を認識する
            face = cascade.detectMultiScale(self._gray, scaleFactor=1.03, minNeighbors=3, minSize=(120, 120))
            # 顔判定
            if 0 < len(face):
                for (x, y, w, h) in face:
                    # 顔の部分だけ切り抜いてモザイク処理をする
                    cut_img = self._image[y:y + h, x:x + w]
                    cut_face = cut_img.shape[:2][::-1]
                    # 10分の1にする
                    cut_img = cv2.resize(
                        cut_img, (cut_face[0] // 25, cut_face[0] // 25))
                    # 画像を元のサイズに拡大
                    cut_img = cv2.resize(cut_img, cut_face, interpolation=0)
                    # モザイク処理した部分を重ねる
                    self._image[y:y + h, x:x + w] = cut_img
                    if self._debug:
                        # 認識部分を四角で囲む
                        cv2.rectangle(self._image, (x, y), (x + w, y + h), (50, 50, 255), 2)
            return len(face)
        except:
            raise
