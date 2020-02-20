README.md

# Public Mapping
====
# Overview
現地調査をもっと手軽に、より共有しやすく</br>
属人化しがちな現地情報を、このアプリを介して簡単・安全に、ワンアクションで記録・共有することで、</br>
情報共有不足によるヒューマンエラーを現場から一掃します！</br>

## Description
プロジェクト名：publicmapping</br>
アプリケーション名：mapping</br>

## Demo
coming soon

## VS.
### google map との違い
・外部への共有機能が排除してあるため、ログインパスワードを知らない他者への情報漏洩の心配がありません。</br>
・クラウドサーバーでなく、特定のサーバーを利用できるため、情報セキュリティ上管理しやすくなっています。</br>
・背景地図をOSM(Open Street Map)か地理院地図かから選択ができるため、商用利用でも費用が発生しません。</br>
・アイコンに番号を振れるため、地図を印刷した場合に、どの地点が何番の情報かひと目でわかります</br>

## Requirement
Python 3.7.4<br/>
Django 3.0.2<br/>
Django Rest Framework 3.11.0<br/>

PostgreSQL 11.5<br/>
postgis 2.5.3<br/>
gdal 2.4.2<br/>
libgeoip 1.6.12<br/>

## Usage 利用方法と画面の名称
・ログイン画面：付与されたユーザー名、パスワードを入力し、ログインできます。</br>
・メインビュー：左側に情報の一覧、右側に地図が表示されます。</br>
  →新規登録ボタンまたは編集ボタンから、新規追加・編集ビューへ。
・新規追加・編集ビュー： 地物の名称、番号、メモ、位置を入力できます。編集においても同様です。</br>
・削除ボタン：登録したデータを削除できます。</br>
・ヘルプボタン：ヘルプ画面を参照できます。</br>
・ログアウトボタン：アプリからログアウトできます。</br>

## 開発状況と今後の方針
### 2/22時点でβ版を公開しています。
### 完成版での実装予定
--バックエンド--</br>
・バグ、不具合の解消</br>

--フロントエンド--</br>
・スタイルの統一</br>
・メインビューでの削除確認ポップアップの不具合修正</br>
・その他バグ、不具合の解消</br>

### 開発終了予定
2020/2/29(土)に完成予定</br>

## Detailed Descriptions of the application
### バックエンド
#### ユーザー登録・ログイン認証について
・ユーザーは管理者がアカウント、パスワードを作成して付与することを想定し、サインアップ機能は実装していない。<br/>
・以下のウェブサイトを参考にUserモデルを(AbstractUser)でカスタマイズした。<br/>
https://noumenon-th.net/programming/2019/11/25/django-abstractuser/ <br/>
・Userモデルが持つ既存の12のフィールド（以下）に変更は加えていない<br/>
username, first_name, last_name, email, password, groups, user_permissions
is_staff, is_active, is_superuser, last_login, date_joined

※ログイン・ログアウトは以下のページのコードを利用 <br/>
https://github.com/toksan/django2_tutorial_blog_with_auth/tree/master/myblog/templates/registration <br/>
ログイン後のREDIRECT先は settings.pyの中に'/map_mainview/'を指定し、ホーム画面に遷移するようにした

#### modelの定義
models.pyのPostクラスに定義されたフィールドは以下の通り<br/>
GeoDjangoのgeometric fieldの一つであるPointFieldを用いて、緯度経度情報を持った位置情報のメモをPost modelとして作成した。<br/>

Fields | Detail
------------ | -------------
title | 地点名称（20文字以内の文字情報）
number | 地点番号（自分で設定できる整数値）
location | 緯度経度情報(世界測地系WGS84に基づく緯度経度、小数値)
number | 地点番号（自分で設定できる整数値）

#### viewsの設定
##### メインビューの設定
左側：postモデルから各オブジェクトを受け取り、テーブルとして表示</br>
右側：GeojsonAPIView(APIView)で生成されたJSONを'js/app.js'で受け取ってleaflet地図として表示</br>

##### CRUDの実装
DjangoでCRUD（https://qiita.com/zaburo/items/ab7f0eeeaec0e60d6b92）</br>
を参考にviews.py内で新規追加(post_add)、編集(post_edit)、削除(post_delete)を定義</br>

##### GeoJSONの生成
APIViewクラスを用いて、全てのPostオブジェクト含むGeojsonを生成するGeojsonAPIView(APIView)クラスを作成した。</br>
Postオブジェクトから位置情報（'location'）とフィールド('title', 'number',)を取得し、JSONファイルを生成し、<project/urls.py>で'mapping/geojson/'というURLを割り当てた。</br>

#### Formの作成
ModelFormを用いてPost modelを取り込み、'title','number','memo', 'location'全てのフィールドのフォームを作成。<br/>
memoフィールドはforms.CharField(widget = forms.Textarea)を使って大きな入力枠を設定<br/>
locationフィールドは以下のページを参照しOSMWidgetを使ってleafletでのインタラクティブな入力画面を設定。<br/>
https://stackoverflow.com/questions/47750850/osmwidget-map-doesnt-show-in-template-referenceerror-ol-is-not-defined<br/>
地図の中心地点は札幌駅[43.06417, 141.34964]、ズームは10に指定<br/>

### フロントエンド
#### CSS & Bootstrap
Bootstrap V4.4.1 の[CDN(Content Delivery Network)](https://www.bootstrapcdn.com)を利用

#### leafletの設定
Leaflet 1.6.0 の[Hosted version](https://leafletjs.com/download.html)を利用

## Contribution
coming soon

## Licence
coming soon

## Author
Hiroaki Ishii</br>
Twitter: [@hiroishi0422](https://twitter.com/hiroishi0422)</br>
Qiita: [@hiro-ishi](https://qiita.com/hiro-ishi)</br>

## Acknowledgment
### Yuu Takahashi
Schedule management, Direction, debug, and advice</br>
Twitter: [@john95206](https://twitter.com/john95206)</br>
Qiita: [@john95206](https://qiita.com/john95206)</br>

### Yusuke Sugamiya
Debug, code review and advice</br>
Website: [dnpp.org](https://dnpp.org)</br>

### Hiroshi Omata
Code review and advice</br>
about.me: [about.me](https://about.me/homata)</br>

### Mamix
Code review and advice</br>

### Y Furukawa
Code review and advice</br>
Qiita: [@Yfuruchin](https://qiita.com/Yfuruchin)</br>

## 参考資料
わかりやすいREADME.mdを書く
https://deeeet.com/writing/2014/07/31/readme/ <br/>
リポジトリのライセンス
https://help.github.com/ja/github/creating-cloning-and-archiving-repositories/licensing-a-repository<br/>
