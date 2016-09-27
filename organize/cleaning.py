# -*- coding: utf-8 -*-
"""写真の整理"""
import os
import configparser
import cv2
from numpy import ndarray

from organize.photo import Photo
import organize.exception as exception


class Cleaning(Photo):
    """写真の整理を行うクラス.
    ライフログとして撮影された大量の写真を整理する役割を持ったクラスです.
    機能は写真のピンボケ判定、連続で作成された写真の類似度を判定.
    また、顔を認識しモザイク化を行います.
    """
    def __init__(self, filename):
        super().__init__(filename)
        # 設定
        self._config = configparser.ConfigParser()
        self._config.read("organize" + os.sep + "config.ini")
        # 初期設置
        self._compare_status = None
        self._blurry_status = None

    # 類似度判定結果
    @property
    def compare_status(self):
        return self._compare_status

    # ピンボケ判定結果
    @property
    def blurry_status(self):
        return self._blurry_status

    def out_of_focus(self, blurry_value: float) -> bool:
        """ピンボケ判定.
        ボケ閾値を指定し画像のボケ具合を判定

        Args:
            blurry_value: リサイズのパーセント指定(例:90.5)
        return:
            判定結果: くっきり = True, ボケている = False
        """
        # エッジ検出
        focus = cv2.Laplacian(self._gray, cv2.CV_64F).var()
        # ピンボケ判定
        if focus >= blurry_value:
            # くっきり
            self._blurry_status = True
        else:
            # ボケている
            self._blurry_status = False
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

    def compare(self, image: ndarray, compare_value: float) -> bool:
        """オリジナル画像と入力画像の類似度判定する.

        Args:
            image: 比較画像
            compare_value: 類似度のパーセント指定(例:90.5)
        return:
            判定結果: 似ている = True, 似ていない = False
        """
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
        if difference >= (compare_value / 100):
            # 似ている
            self._compare_status = True
        else:
            # 似ていない
            self._compare_status = False
        # Debug
        if self._debug:
            color = (238, 110, 64)
            print("- {}: {:.2f}%".format("Compare: ", float(difference) * 100))
            cv2.putText(self._image, "{}: {:.2f}%".format("Compare: ", float(difference) * 100),
                        (50, self.debug_text_y()), cv2.FONT_HERSHEY_SIMPLEX, 2.0, color, 3)
        return self._compare_status

    def mosaic(self):
        """モザイク.
        設定ファイル(config.ini)の[cascade_file]セクションに定義されているカスケードファイルを読み込みに画像から該当する対象に
        モザイクを適用する。カスケードファイルは[cascade_file]に定義されている全てが適用される
        """
        try:
            # TODO パフォーマンス改善ポイント
            for key in self._config['cascade_file']:
                file = self._config['cascade_file'][key]
                face = self.__cascade(file)
                if self._debug:
                    color = (238, 110, 64)
                    print("- {}: {:5d}".format(key, face))
                    cv2.putText(self._image, "{}: {:d}".format(key, face), (50, self.debug_text_y()),
                                cv2.FONT_HERSHEY_SIMPLEX, 2.0, color, 3)
        except KeyError:
            raise exception.Photo_setting_exception

    def __cascade(self, cascade_file: str) -> int:
        """顔認識.
        カスケードファイルを用いて顔を認識しモザイク処理を施す

        Args:
            cascade_file: 処理対象のカスケードファイル
        return:
            顔の検出数
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
                minSize – 物体が取り得る最小サイズ．これよりも小さい物体は無視されます
            """
            # カスケード分類器の設定
            factor = float(self._config['detect_multi_scale']['SCALE_FACTOR'])
            neighbors = int(self._config['detect_multi_scale']['MIN_NEIGHBORS'])
            min_size_x = int(self._config['detect_multi_scale']['MIN_SIZE_X'])
            min_size_y = int(self._config['detect_multi_scale']['MIN_SIZE_Y'])
            face = cascade.detectMultiScale(
                self._gray,
                scaleFactor=factor,
                minNeighbors=neighbors,
                minSize=(min_size_x, min_size_y)
            )
            # 顔判定
            if 0 < len(face):
                for (x, y, w, h) in face:
                    # 顔の部分だけ切り抜いてモザイク処理をする
                    cut_img = self._image[y:y + h, x:x + w]
                    cut_face = cut_img.shape[:2][::-1]
                    # 縮小
                    cut_img = cv2.resize(
                        cut_img, (cut_face[0] // 20, cut_face[0] // 20))
                    # 画像を元のサイズに拡大
                    cut_img = cv2.resize(cut_img, cut_face, interpolation=0)
                    # モザイク処理した部分を重ねる
                    self._image[y:y + h, x:x + w] = cut_img
                    if self._debug:
                        # 認識部分を四角で囲む
                        cv2.rectangle(self._image, (x, y), (x + w, y + h), (180, 180, 230), 2)
            return len(face)
        except Exception:
            raise exception.Photo_cascade_exception
