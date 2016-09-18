# -*- coding: utf-8 -*-
"""
写真基底クラス
"""
import cv2
import configparser
import os.path
import shutil

from photo.photo import Photo
from photo.cleaning import Cleaning


def main():
    """
    debugがTrueの場合、ピンボケ判定値、顔認識エリア、類似度を出力画像に描写、元写真はそのまま残ります
    TODO
        .DS_*など不要なファイルの削除
        動画の移動
        クラス化
        タイムラスプ出力
    :return:
    """
    # 設定
    config = configparser.ConfigParser()
    config.read('config.ini')
    debug = config['setting']['debug']
    input_dir = config['setting']['input_dir']
    output_public_base_dir = config['setting']['public_dir']
    output_private_base_dir = config['setting']['private_dir']
    backup_base_dir = config['setting']['backup_dir']
    trash_base_dir = config['setting']['trash_dir']
    blurry_value = config['setting']['blurry_value']
    compare_value = config['setting']['compare_value']

    compare_image = None
    compare_status = True

    try:
        # 画像処理
        for root, dirs, files in os.walk(input_dir):
            for file in files:
                if file.endswith(".jpg"):
                    # 処理対象のファイルを取得
                    input_file = os.path.join(root, file)
                    # 写真整理の生成
                    photo = Cleaning(input_file)
                    photo.debug(debug)
                    # 写真の撮影日を取得（保存ディレクトリに使用）
                    date = photo.shooting_date()
                    # ピンボケ判定
                    blurry_status = photo.out_of_focus(blurry_value)
                    # 前の写真と類似判定
                    if blurry_status and compare_image is not None:
                        compare_status = photo.compare(compare_image, compare_value)
                    # 保存判定
                    if blurry_status and compare_status:
                        if output_private_base_dir is not None:
                            """ プライベートなディレクトリに保存 """
                            output_private_file = os.path.join(_make_directory(output_private_base_dir, date), file)
                            photo.save(output_private_file)
                            print('OK(Public dir save): ' + output_private_file)
                        if output_public_base_dir is not None:
                            """ モザイクを施し公開用ディレクトリに保存 """
                            photo.mosaic()
                            output_public_file = os.path.join(_make_directory(output_public_base_dir, date), file)
                            photo.save(output_public_file)
                            print('OK(Public dir save): ' + output_public_file)
                        # 類似判定用画像取得
                        compare_image = photo.original
                    else:
                        if trash_base_dir is not None:
                            """ 破棄用写真の保管 """
                            trash_file = os.path.join(_make_directory(trash_base_dir, date), file)
                            photo.save(trash_file)
                            print('NG(Trash dir save): ' + trash_file)
                    if debug.lower() == "false":
                        if backup_base_dir is not None:
                            """ 入力写真をバックアップディレクトリに移動 """
                            backup_dir = _make_directory(backup_base_dir, date)
                            shutil.move(input_file, backup_dir)
            remaining_files = os.listdir(root)
            if len(remaining_files) == 0:
                """ 入力ディレクトリにファイルが存在しない場合はディレクトリ削除 """
                os.remove(root)
                print("Dir delete: " + root)

    except Exception as e:
        print('ERROR')
        print(' type:' + str(type(e)))
        print(' args:' + str(e.args))
        print(' exception:' + str(e))

def thumbnail():
    # 設定
    config = configparser.ConfigParser()
    config.read('config.ini')
    reduced_size = config['thumbnail']['reduced_size']
    number_horizontal = config['thumbnail']['number_horizontal']
    debug = config['setting']['debug']
    input_dir = config['setting']['input_dir']
    blank_image = config['setting']['blank_image']
    try:
        # 画像処理
        for root, dirs, files in os.walk(input_dir):
            result = None
            photos_buff = None
            horizon_photos = []
            photo_cnt = 0
            for file in files:
                if file.endswith(".jpg"):
                    photo_cnt += 1
                    # 処理対象のファイルを取得
                    input_file = os.path.join(root, file)
                    # 写真整理の生成
                    photo = Photo(input_file)
                    photo.debug(debug)
                    # 写真の撮影日を取得（保存ディレクトリに使用）
                    date = photo.shooting_date()
                    # 画像縮小
                    # resize_photo = photo.resize(reduced_size)
                    photo.resize(reduced_size)
                    # 写真の枠を追加
                    photo.edges()
                    # 加工済み写真の取得
                    resize_photo = photo.image
                    if photos_buff is None:
                        photos_buff = resize_photo
                    else:
                        # 横方向の連結
                        photos_buff = cv2.hconcat([photos_buff, resize_photo])
                    if photo_cnt >= int(number_horizontal):
                        horizon_photos.append(photos_buff)
                        photos_buff = None
                        photo_cnt = 0
            else:
                if photos_buff is not None:
                    margin_photo = Photo(blank_image)
                    margin_photo.resize(reduced_size)
                    resize_photo = margin_photo.image
                    while photo_cnt < int(number_horizontal):
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
            cv2.imwrite('thumbnail.png', result)

    except Exception as e:
        print('ERROR')
        print(' type:' + str(type(e)))
        print(' args:' + str(e.args))
        print(' exception:' + str(e))

def move_files():
    # 設定
    config = configparser.ConfigParser()
    config.read("config.ini")
    input_dir = config["setting"]["input_dir"]
    output_public_base_dir = config["setting"]["public_dir"]
    target_files = config["setting"]["move_files"]
    target_files = tuple(target_files.split(","))
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith(target_files):
                # 処理対象のファイルを取得
                input_file = os.path.join(root, file)
                # ファイル名から保存先ディレクトリを指定
                dir_name = file[0:4]+"-"+file[4:6]+"-"+file[6:8]
                # ファイルの移動
                output_dir = _make_directory(output_public_base_dir, dir_name)
                shutil.move(input_file, output_dir)

def delete_unneeded_files():
    # 設定
    config = configparser.ConfigParser()
    config.read("config.ini")
    input_dir = config["setting"]["input_dir"]
    target_files = config["setting"]["delete_files"]
    target_files = tuple(target_files.split(","))
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith(target_files):
                # 処理対象のファイルを取得
                input_file = os.path.join(root, file)
                os.remove(input_file)

def _make_directory(directory, date):
    """
    指定されたディレクトリ配下に日付を付加したディレクトリを返却（存在しない場合は作成）
    :param directory:
    :param date:
    :return:
    """
    output_directory = directory + os.sep + date[:4] + os.sep + date[5:7] + os.sep + date
    if not os.path.isdir(output_directory):
        os.makedirs(output_directory)
    assert isinstance(output_directory, str)
    return output_directory

if __name__ == '__main__':
    main()
    thumbnail()
    move_files()
