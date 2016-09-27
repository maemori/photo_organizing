# -*- coding: utf-8 -*-
"""写真の整理で共通で利用できる機能."""
import os
import shutil


def files(func, target_dir: object):
    """指定されたディレクトリ配下にある画像を処理するレコレーター.
    """
    def target_function(*args: tuple, **kwargs: dict):
        result = []
        for root, dirs, fileset in os.walk(target_dir):
            for file in fileset:
                target_file = os.path.join(root, file)
                result += [func(target_file, *args, **kwargs)]
        return result

    return target_function


def copy(target_file: str, output_dir: str):
    """ファイルのコピー.
    """
    shutil.copy(target_file, output_dir)
    return target_file


def delete(target_file: str):
    """ファイルの削除.
    """
    os.remove(target_file)
    return target_file
