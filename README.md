# photo_organizing
Application to organize a large number of photos
(大量の写真を整理するアプリケーション)

## 0.はじめに

![Narrative Clip 2](http://getnarrative.com/assets/images/box.png)

ライフログカメラの「[Narrative Clip 2](http://getnarrative.com/)」(ナラティブ クリップ 2)を使用すると30秒に1枚自動で撮影してくれます。
朝から晩まで（16時ほど）首からぶら下げていると約2,000枚ほどその間の出来事を写真として保存してくれます。
旅行や散歩、居酒屋巡りなど強い味方なのですが、この2,000枚の写真の中にはブレているものや同じようなものなどライフログとしてはノイズ的な写真が多くその日の出来事がそのノイズに埋もれてしましライフログの価値を下げてしまっています。 (写真をネット上にアップする際に一々人の顔にモザイクをかけるのも手間)

当機能はそのノイズを除去しライフログとしての価値を高めることを目的としています。

### 適用前の状態

### 適用後の状態

## 1.機能概要

* 類似写真の除去
* ブイている写真の除去
* 顔をモザイク化
* サムネイルの作成

## 2.動作環境

* Python 3.5
* OpenCV 2.4

## 3.設定

[Wiki参照](https://github.com/maemori/photo_organizing/wiki)

## 4.実行方法

```
$ python main.py
```


