# -*- coding: utf-8 -*-
"""写真の整理で共通で利用できる機能."""
import os
import shutil


def files(func, target_dir: object):
    """指定されたディレクトリ配下にある画像を処理するレコレーター."""
    def target_function(*args: tuple, **kwargs: dict):
        result = []
        for root, dirs, fileset in os.walk(target_dir):
            for file in fileset:
                target_file = os.path.join(root, file)
                result.append(func(target_file, *args, **kwargs))
        return result

    return target_function


def copy(target_file: str, output_dir: str) -> str:
    """ファイルのコピー."""
    # ディレクトリが存在しない場合は作成
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)
    # コピー
    shutil.copy(target_file, output_dir)
    return target_file


def delete(target_file: str) -> str:
    """ファイルの削除."""
    # 削除
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


def delete_directory(target_dir: str):
    """指定ディレクトリ配下の空ディレクトリを削除."""
    delete_dir_pass = []
    try:
        for root, dirs, fileset in os.walk(target_dir):
            for dir_name in dirs:
                dir_pass = os.path.join(root, dir_name)
                if os.path.isdir(dir_pass):
                    delete_dir_pass.append(dir_pass)
        delete_dir_pass.reverse()
        for test in delete_dir_pass:
            os.removedirs(test)
    except OSError:
        pass
