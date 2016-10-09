# -*- coding: utf-8 -*-
"""写真の整理"""
import os
import configparser
import cv2
from numpy import ndarray

from organize.photo import Photo
import organize.exception as exception
import everyone.log as log
import everyone.performance as performance


class Cleaning(Photo):
    """写真の整理を行うクラス.
    ライフログとして撮影された大量の写真を整理する役割を持ったクラスです.
    機能は写真のピンボケ判定、連続で作成された写真の類似度を判定.
    顔を認識しモザイク化を行います.
    """
    # 写真分析結果出力用ログ
    analysis_log = log.logger("analysis")

    _CONFIG = {}
    _CASCADE = {}

    def __init__(self, filename):
        super().__init__(filename)
        # 設定の読み込み（シンングルトン）
        Cleaning.config()
        Cleaning.cascade()
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

    @classmethod
    def config(cls):
        """設定を取得して保持する
        """
        if not cls._CONFIG:
            try:
                super().log.info("Config file read")
                config = configparser.ConfigParser()
                config.read(os.path.join("conf", "organize", "config.ini"))
                # カスケード分類器の設定
                cls._CONFIG["factor"] = float(config["detect_multi_scale"]["SCALE_FACTOR"])
                cls._CONFIG["neighbors"] = int(config["detect_multi_scale"]["MIN_NEIGHBORS"])
                cls._CONFIG["min_size_x"] = int(config["detect_multi_scale"]["MIN_SIZE_X"])
                cls._CONFIG["min_size_y"] = int(config["detect_multi_scale"]["MIN_SIZE_Y"])
                cls._CONFIG["cascade_file"] = config["cascade_file"]
            except (KeyError, ValueError):
                raise exception.Photo_setting_exception

    @classmethod
    def cascade(cls):
        """顔探索用のカスケード型分類器を取得し保持する
        """
        if not cls._CASCADE:
            try:
                super().log.info("Cascade files read")
                for key in cls._CONFIG["cascade_file"]:
                    file = cls._CONFIG["cascade_file"][key]
                    cls._CASCADE[key] = cv2.CascadeClassifier(file)
            except KeyError:
                raise exception.Photo_setting_exception

    @performance.time_func
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
        # 分析用ログ出力
        self.analysis_log.info(
            "Filename:{Filename}, Clearly status:{Clearly:s}, Blurry:{Blurry_value:.2f}, Focus:{Focus:.2f}"
            .format(Filename=self.filename, Clearly=str(self._blurry_status), Blurry_value=blurry_value, Focus=focus))
        return self._blurry_status

    @performance.time_func
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
        difference = float(float(total) / sum(this_histogram))
        if difference >= (compare_value / 100):
            # 似ている
            self._compare_status = True
        else:
            # 似ていない
            self._compare_status = False
        # 分析用ログ出力
        self.analysis_log.info(
            "Filename:{Filename}, Compare status:{Compare_status:s}, Compare{Compare:.2f}, Difference:{Difference:.2f}"
            .format(Filename=self.filename, Compare_status=str(self._compare_status), Compare=(compare_value / 100),
                    Difference=difference))
        return self._compare_status

    @performance.time_func
    def mosaic(self):
        """モザイク.
        設定ファイル(config.ini)の[cascade_file]セクションに定義されているカスケードファイルを読み込みに画像から該当する対象に
        モザイクを適用する。カスケードファイルは[cascade_file]に定義されている全てが適用される
        """
        try:
            for key in self._CASCADE.keys():
                face = self._cascade_func(self._CASCADE[key])
                # 分析用ログ出力
                self.analysis_log.info(
                    "Filename:{Filename}, Cascade:{Cascade:s}, Face:{Face:d}"
                    .format(Filename=self.filename, Cascade=str(key), Face=face))
        except Exception:
            raise

    @performance.time_func
    def _cascade_func(self, cascade: cascade) -> int:
        """顔認識.
        カスケードファイルを用いて顔を認識しモザイク処理を施す

        Args:
            cascade: 処理対象のカスケード
        return:
            顔の検出数
        """
        try:
            """
            物体認識（顔認識）の実行
                image – CV_8U 型の行列．ここに格納されている画像中から物体が検出されます
                objects – 矩形を要素とするベクトル．それぞれの矩形は，検出した物体を含みます
                scaleFactor – 各画像スケールにおける縮小量を表します
                minNeighbors – 物体候補となる矩形は，最低でもこの数だけの近傍矩形を含む必要があります
                minSize – 物体が取り得る最小サイズ．これよりも小さい物体は無視されます
            """
            face = cascade.detectMultiScale(
                self._gray,
                scaleFactor=self._CONFIG["factor"],
                minNeighbors=self._CONFIG["neighbors"],
                minSize=(self._CONFIG["min_size_x"], self._CONFIG["min_size_y"])
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
        except KeyError:
            raise exception.Photo_setting_exception
        except Exception:
            raise exception.Photo_cascade_exception
