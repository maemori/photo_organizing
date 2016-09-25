# -*- coding: utf-8 -*-
"""共通で利用できる機能."""
import os
import shutil


def files(func, target_dir: object):
    """指定されたディレクトリ配下にある画像を処理するレコレーター.
    """
    def target_function(*args: tuple, **kwargs: dict):
        for root, dirs, files in os.walk(target_dir):
            for file in files:
                target_file = os.path.join(root, file)
                func(target_file, *args, **kwargs)

    return target_function


def photo_files(func, target_dir: object):
    """指定されたディレクトリ配下にある画像を処理するレコレーター.
    """
    def target_function(*args: tuple, **kwargs: dict):
        for root, dirs, files in os.walk(target_dir):
            for file in files:
                if not file.endswith('.jpg'):
                    continue
                target_file = os.path.join(root, file)
                func(target_file, *args, **kwargs)

    return target_function


def copy(target_file: str, output_dir: str):
    """ファイルのコピー.
    """
    shutil.copy(target_file, output_dir)


def delete(target_file: str):
    """ファイルの削除.
    """
    os.remove(target_file)
