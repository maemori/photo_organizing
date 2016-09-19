# photo_organizing
Application to organize a large number of photos
(大量の写真を整理するアプリケーション)

## 0.はじめに

![Narrative Clip 2](http://getnarrative.com/assets/images/box.png)

ライフログカメラの「[Narrative Clip 2](http://getnarrative.com/)」(ナラティブ クリップ 2)を使用すると30秒に1枚自動で撮影してくれます。
朝から晩まで（16時ほど）首からぶら下げていると約2,000枚ほどその間の出来事を写真として保存。
旅行や散歩、居酒屋巡りなど強い味方なのですが、この2,000枚の写真の中にはブレているものや同じようなものなどライフログとしてはノイズ的な写真が多くその日の出来事がそのノイズに埋もれてしましライフログの価値を下げてしまっています。 (写真をネット上にアップする際に一々人の顔にモザイクをかけるのも手間)

当機能はそのノイズを除去しライフログとしての価値を高めることを目的として開発雨を行っております。

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

### 4.1.実行したサンプル

とある１日にNarrative Clip 2を首からぶら下げて撮影された写真たちを使用。実効後は撮影日毎に設定された出力先にディレクトリが作成されここの写真とサムネイルが保存されます。（約540枚→約200枚）

#### 4.1.1.適用前の状態（約540枚）

![適用前](https://github.com/maemori/photo_organizing/blob/master/test/thumbnail_before.png?raw=true)

#### 4.1.2.適用後の状態（約200枚）

![適用後](https://github.com/maemori/photo_organizing/blob/master/test/thumbnail_after.png?raw=true)

