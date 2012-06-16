# なめこ収穫スクリプト

## 概要

このスクリプトは、某なめこを収穫するだけのMonkeyRunnerスクリプトです。

MonkeyRunnerスクリプトのサンプルであり、乱用はゲーム本来の楽しみを損ないます。くれぐれもcrontabに登録して使用することは絶対におやめください。

※怒られたら消します。

#### できること
- なめこの収穫
- フード追加

#### できないこと
- 設備の購入
- かび取り


## 実行方法

### Jenkinsからのデバイス指定実行
ジョブを「マルチ構成プロジェクトのビルド」で作成し、以下のように設定すると指定したシリアル番号のデバイスで順に実行します。

- ビルド・トリガ：定期的に実行
- マトリックスの設定→軸の追加→ユーザ定義で、名前を"serial"、値にadb devicesコマンドで得られるシリアル番号をスペース区切りで指定
- ビルド手順の追加→シェルの実行で"monkeyrunner namekoharvest.py"を指定（フルパス）

### Jenkinsからの全デバイス実行
ジョブを「フリースタイル・プロジェクトのビルド」で作成し、以下のように設定すると接続されている全デバイスで順に実行します。

- ビルド・トリガ：定期的に実行
- ビルド手順の追加→シェルの実行で"monkeyrunner namekoharvest.py"を指定（フルパス）

### コマンドラインからの実行
コマンドラインで下記コマンドを実行すると接続されている全デバイスで順に実行します。

$ monkeyrunner namekoharvest.py（フルパス）


## 動作確認機種
- Nexus One
- Galaxy S II
- Galaxy Nexus
- ICONIA Tab A500


## monkeyrunnerについて
MonkeyRunnerは、AndroidSDKに同梱のUIテスト用フレームワークです。詳しくは下記URLを参照してください。

http://developer.android.com/guide/developing/tools/monkeyrunner_concepts.html


## monkeyutils.pyについて
同梱のmonkeyutils.pyはこちらで公開されているものを使用しています。このモジュールにより、単一のスクリプトで多様な解像度の端末で（だいたい）動作します。

https://sites.google.com/site/androidtestclub/