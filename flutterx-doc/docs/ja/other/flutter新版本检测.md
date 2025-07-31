# Flutter新バージョン検出


Flutterプロジェクトを開く際にデフォルトでプロセスが起動し、HTTPリクエストが発行され、Flutterバージョン情報のインターフェースにアクセスします。


リクエストURL

> URL: [https://storage.googleapis.com/flutter_infra_release/releases/releases_macos.json](https://storage.googleapis.com/flutter_infra_release/releases/releases_macos.json)


> インターフェースにアクセスするにはプロキシを有効にする必要があります。


## スクリーンショットプレビュー

![image_9.png](/images/image_9.png)

![image_10.png](/images/image_10.png)

whats new はFlutter GitHubリポジトリのCHANGELOG.mdファイルにジャンプします。

## 機能が必要とする2つの条件

新バージョンチェックには2つの条件が必要です。

* Flutterコマンドが正常に呼び出せること
* 上記URLインターフェースに正常にアクセスできること

## この機能が不要な場合、ここで無効化してください。

![image_8.png](/images/image_8.png)
