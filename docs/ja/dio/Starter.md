# Dioリクエスト監視

## 1.ウィンドウプレビュー

このウィンドウが見つからない場合は、デフォルトで表示されていない可能性があります。メニューバーで手動で開く必要があります: `View -> Tool Windows -> Dio Request`

![dio windows](/images/dio/_dio_01.png)

## 2.サービス実行状態

緑の点が表示されている場合、サービスが実行中であることを示し、接続して使用を開始できます。

![status](/images/dio/img_2.png)

## 3.使用開始

[![Pub Version (including pre-releases)](https://img.shields.io/pub/v/dd_check_plugin)](https://pub.dev/packages/dd_check_plugin)

#### 依存関係の追加

```yaml
 dd_check_plugin: ^lastVersion
```

#### 依存関係の取得

```bash
flutter pub get
```

#### コードの作成

Dioのシングルトンクラスを渡してください。プラグインはインターセプターを追加してリクエストを監視し、リクエストモデルをFlutterXプラグインに送信します。

```dart
    void main(){
    DdCheckPlugin().init(Dio(),
        initHost: "192.168.100.63",
        port: 9999,
        projectName: 'App Name');
}
```

> **説明**
>
> この機能の実装原理を簡単に説明します。FlutterXプラグイン側ではSocketサーバーが実行されており、DdCheckPlugin#init関数のinitHostを通じて接続し、
> データ転送を行います。[ソースコードの一部:](https://github.com/mdddj/dd_flutter_idea_plugin/blob/d5a57dcf769fd59c383fd89d21e6f6503bff948c/src/main/kotlin/shop/itbug/fluttercheckversionx/socket/service/DioApiService.kt#L112)

以下は`DdCheckPlugin#init`関数のいくつかのプロパティの説明です。

| パラメータ | 説明 |
|---|---|
| initHost | あなたのローカルIPアドレスを設定してください。127.0.0.1に設定しないでください。実機モードでは接続できません。「1」を入力するとプラグインが自動補完を行います。選択してください。 |
| port | リッスンポート、デフォルトは9999で、設定で変更できます。特別な要件がない場合は変更しないでください。この設定を変更した後はASを再起動してください。 |
| projectName | プロジェクト名をカスタマイズしてください。 |
| customCoverterResponseData | IDEに送信されるデータモデルを変更できます。特別なことはない場合は変更する必要はありません。しかし、追加の備考情報を追加できます。 |
| timeOut | IDEプラグインへの接続タイムアウト時間 |
| hostHandle | initHostを渡さない場合、関数はIPセグメントをスキャンして自動接続を試みます。通常は使用しません。 |
| version | データ転送形式のバージョン、通常は変更する必要はありません。 |
| conectSuccess | プラグインへの接続成功時のコールバック、接続socketオブジェクトをコールバックします。通常は使用しません。 |
| extend | その他のツール拡張、例えばHiveツールの拡張: `HiveToolManager` も実装できます。`ServerMessageHandle`インターフェースを実装して、IDEプラグインから送信されたデータを処理することもできます。 |


## 4.initHostの自動補完

プラグインは自動的にIPアドレスを識別し、ヒントを提供します。

![img_3.png](/images/dio/img_3.png)

## 5.インターフェースに備考を追加

> **注意**
>
> FlutterXバージョン3.8.0+が必要です。

`customCoverterResponseData`プロパティを使用して、IDEに送信するresponseモデルをカスタマイズします。
下の例を見てください。

```dart
    DdCheckPlugin().init(
        BaseApi.getDio(),
        customCoverterResponseData: _customCoverterResponseData
);

SendResponseModel _customCoverterResponseData(SendResponseModel sendResponseModel) {
  final notes = <String>[];
  if (sendResponseModel.url.contains("/tkapi/api/v1/dtk/apis/goods")) {
    notes.add("ホーム製品リストインターフェース");
  } else if (sendResponseModel.url.contains("/tkapi/api/v1/dtk/apis/carousel-list")) {
    notes.add("カルーセル図インターフェース");
  } else if (sendResponseModel.url.contains("/api/get-user-by-token")) {
    notes.add("トークンを使用したユーザー情報モデルの取得");
  }
  notes.add("${sendResponseModel.response?.data.runtimeType}"); //response戻り値の型を追加
  return sendResponseModel.copyWith(extendNotes: notes);
}
```

効果は図の通りです。`SendResponseModel#extendNotes`内の文字列配列がURLでループされ、タグとして表示されます。

![img_4.png](/images/dio/img_4.png)

備考が多すぎる場合は、ワイドモードで表示することをお勧めします。

![img_5.png](/images/dio/img_5.png)

これは私の設定です。

![img_6.png](/images/dio/img_6.png)

## 6. Json to Freezed モデル

> freezedが何かわからない場合は、強く理解することをお勧めします。[リンク](https://pub.dev/packages/freezed)

特定のインターフェースを選択し、このアイコンをクリックすると、json to freezedモデルの設定ポップアップが表示されます。
または、インターフェースを右クリックしてポップアップメニューからもこのオプションを選択できます。

![img_7.png](/images/dio/img_7.png)

![img_8.png](/images/dio/img_8.png)

![img_9.png](/images/dio/img_9.png)
