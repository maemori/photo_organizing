# -*- coding: utf-8 -*-
"""複数の写真をまとめて整理"""
import configparser
import os.path
import shutil

import cv2

from organize.base import Base
import organize.exception as exception
from organize.cleaning import Cleaning
from organize.photo import Photo
import everyone.util as util
import everyone.performance as performance


class Photos(Base):
    """複数の写真をまとめて整理するクラス"""
    def __init__(self):
        # 設定の読み込み
        super().log.info("Config file read")
        self.config = Config()
        # 類似画像比較結果
        self.compare_status = True
        # 比較用保持画像
        self.compare_image = None
        # 処理結果保存ディレクトリ
        self.create_directory = []

    @performance.time_func
    def organize(self):
        """写真整理メイン処理"""
        try:
            # 写真の整理を行うメイン処理
            processor = util.files(self._organize_func, self.config.input_dir)
            processor()
            # 移動対象ファイルを処理
            processor = util.files(self._move_files_func, self.config.input_dir)
            processor()
            # 削除対象ファイルを処理
            processor = util.files(self._delete_unneeded_func, self.config.input_dir)
            processor()
            # サムネイル画像の出力
            self.thumbnail()
            # 入力ディレクトリの空ディレクトリを削除
            self._delete_directory()
        except exception.Photo_exception as ex:
            super().log.error('Exception type{Type:s}, Args{Args:s}, Detail{Detail:s}'
                              .format(Type=str(type(ex)), Args=str(ex.args), Detail=str(ex)))

    @performance.time_func
    def _organize_func(self, target_file: str):
        try:
            if not target_file.endswith(".jpg"):
                return
            # 写真整理の生成
            photo = Cleaning(target_file)
            # デバッグモード設定
            photo.debug = self.config.debug
            # 写真の撮影日を取得（保存ディレクトリに使用）
            date = photo.shooting_date()
            # ピンボケ判定
            blurry_status = photo.out_of_focus(self.config.blurry_value)
            # バックアップの作成
            if self.config.backup_dir:
                # バックアップの指定がある場合はそのディレクトリに移動
                backup_dir = util.make_directory(self.config.backup_dir, date)
                if not os.path.isfile(backup_dir + os.sep + os.path.basename(target_file)):
                    shutil.move(target_file, backup_dir)
            # 前の写真と類似判定
            if blurry_status and self.compare_image is not None:
                self.compare_status = photo.compare(self.compare_image, self.config.compare_value)
            # 保存判定
            if blurry_status and self.compare_status:
                # 整理済みの写真を指定ディレクトリに保存
                if self.config.output_dir:
                    if self.config.mosaic:
                        # モザイクを施し公開用ディレクトリに保存
                        photo.mosaic()
                    output_directory = util.make_directory(self.config.output_dir, date)
                    output_file = os.path.join(output_directory, os.path.basename(target_file))
                    if output_directory not in self.create_directory:
                        self.create_directory += [output_directory]
                    photo.save(output_file)
                    print('OK(Save): ' + output_file)
                # 類似判定用画像を保持
                self.compare_image = photo.original
            elif self.config.trash_dir:
                # 破棄対象の写真を残す場合は指定のディレクトリに保存
                trash_file = os.path.join(
                    util.make_directory(self.config.trash_dir, date), os.path.basename(target_file))
                photo.save(trash_file)
                print('NG(Trash): ' + trash_file)
            else:
                # 写真の削除
                os.remove(target_file)
        except exception.Photo_exception:
            raise

    @performance.time_func
    def thumbnail(self):
        """サムネイル画像の作成.
        指定されたディレクトリに存在する写真を集めサムネイル画像を作成する.
        """
        try:
            # 画像処理
            for directory in self.create_directory:
                files = os.listdir(directory)
                result = None
                photos_buff = None
                horizon_photos = []
                photo_cnt = 0
                for file in files:
                    if not file.endswith(".jpg"):
                        continue
                    photo_cnt += 1
                    # 処理対象のファイルを取得
                    input_file = os.path.join(directory, file)
                    # 写真整理の生成
                    photo = Photo(input_file)
                    # 画像縮小
                    photo.resize(self.config.thumbnail_reduced_size)
                    # 写真の枠を追加
                    photo.edges()
                    # 加工済み写真の取得
                    resize_photo = photo.image
                    if photos_buff is None:
                        photos_buff = resize_photo
                    else:
                        # 横方向の連結
                        photos_buff = cv2.hconcat([photos_buff, resize_photo])
                    if photo_cnt >= int(self.config.thumbnail_number_horizontal):
                        horizon_photos.append(photos_buff)
                        photos_buff = None
                        photo_cnt = 0
                else:
                    if photos_buff is not None:
                        margin_photo = Photo(self.config.thumbnail_blank_image)
                        margin_photo.resize(self.config.thumbnail_reduced_size)
                        resize_photo = margin_photo.image
                        while photo_cnt < int(self.config.thumbnail_number_horizontal):
                            photos_buff = cv2.hconcat([photos_buff, resize_photo])
                            photo_cnt += 1
                        # 横方向の連結
                        horizon_photos.append(photos_buff)
                    if len(horizon_photos) > 0:
                        for photos_line in horizon_photos:
                            if result is None:
                                result = photos_line
                            else:
                                # 縦方向の連結
                                result = cv2.vconcat([result, photos_line])
                    cv2.imwrite(directory + os.sep + self.config.thumbnail_filename, result)
        except Exception:
            raise exception.Photo_thumbnail_exception

    @performance.time_func
    def _move_files_func(self, target_file: str):
        """入力ディレクトリに存在する処理対象外のファイルを出力ディレクトリに移動する.

        Args:
            target_file: 処理対象のファイル.
        return:
        """
        try:
            extension = tuple(self.config.move_files.split(","))
            if not target_file.endswith(extension):
                return
            # ファイル名から保存先ディレクトリを指定
            target_file_name = os.path.basename(target_file)
            dir_name = target_file_name[0:4] + "-" + target_file_name[4:6] + "-" + target_file_name[6:8]
            # ファイルの移動
            output_dir = util.make_directory(self.config.output_dir, dir_name)
            if not os.path.isfile(output_dir + os.sep + target_file_name):
                shutil.move(target_file, output_dir)
        except Exception:
            raise exception.Photo_exception

    @performance.time_func
    def _delete_unneeded_func(self, target_file: str):
        """入力ディレクトリに存在する除外対象のファイルを削除する.
        Args:
            target_file: 処理対象のファイル.
        return:
        """
        try:
            extension = tuple(self.config.delete_files.split(","))
            if not target_file.endswith(extension):
                return
            # ファイルの削除
            os.remove(target_file)
        except Exception:
            raise exception.Photo_exception

    def _delete_directory(self):
        """入力ディレクトリの空ディレクトリを削除."""
        try:
            os.removedirs(self.config.input_dir)
        except OSError:
            pass


class Config:
    """設定クラス"""
    def __init__(self):
        try:
            config = configparser.ConfigParser()
            config.read('config.ini')
            self.debug = config['setting']['debug']
            self.input_dir = config['setting']['input_dir']
            self.output_dir = config['setting']['output_dir']
            self.backup_dir = config['setting']['backup_dir']
            self.trash_dir = config['setting']['trash_dir']
            self.blurry_value = float(config['setting']['blurry_value'])
            self.compare_value = float(config['setting']['compare_value'])
            self.move_files = config["setting"]["move_files"]
            self.delete_files = config["setting"]["delete_files"]
            # mosaic = config["setting"]["mosaic"].lower()
            if config["setting"]["mosaic"].lower() == 'true':
                self.mosaic = True
            else:
                self.mosaic = False
            self.thumbnail_reduced_size = config['thumbnail']['reduced_size']
            self.thumbnail_number_horizontal = config['thumbnail']['number_horizontal']
            self.thumbnail_blank_image = config['thumbnail']['blank_image']
            self.thumbnail_filename = config['thumbnail']['filename']
        except KeyError:
            raise exception.Photo_setting_exception


if __name__ == '__main__':
    target = Photos()
    target.organize()
