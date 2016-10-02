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


def make_directory(directory: str, date: str) -> str:
    """指定されたディレクトリ配下に日付ディレクトリを返却（存在しない場合は作成）.
    作成されるディレクトリ: ./基準ディレウトリ/[YYYY]/[MM]/[YYYY-MM-DD]

    Args:
        directory: 基準となるディレクトリ.
        date: 基準となるディレクトリ配下に作成する日付情報.
    return:
        ディレクトリパス.
    """
    output_directory = directory + os.sep + date[:4] + os.sep + date[5:7] + os.sep + date
    if not os.path.isdir(output_directory):
        os.makedirs(output_directory)
    assert isinstance(output_directory, str)
    return output_directory
