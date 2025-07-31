# Hive キャッシュ表示ツール

## 1.使い方

プロジェクトに依存関係`dd_check_plugin`を追加し、適切な場所で接続を初期化する必要があります。

```dart
    void main(){
    DdCheckPlugin().init(Dio(),
        initHost: "192.168.100.63", //あなたのコンピュータのIPに変更してください
        port: 9999, //プラグインリッスンポート
        projectName: 'App Name',
        extend: [
            HiveToolManager(boxList: [
              // 重要なコードはここに追加してください。DdPluginHiveBox抽象クラスを実装する必要があります
            ])
    ]);
}
```


`DdPluginHiveBox`クラスの定義

```javascript
abstract class DdPluginHiveBox<T> {
  final String boxName;

  DdPluginHiveBox(this.boxName);

  Future<Box<T>> get getBox;
}

```

> なぜ手動で`getBox`関数を実装する必要があるのか説明します。Hiveがボックスを開く際、デフォルトではTジェネリックを渡さず、dynamic型がデフォルトになります。これによりHiveを開くとエラーが発生します。


| 属性      | 説明          |
|---------|-------------|
| boxName | あなたのHiveボックス名 |
| getBox  | ボックスオブジェクトを返す      |


## 2. 使用例

パネルには3列があります。第1列はボックスリスト、第2列は第1列で選択されたボックス内のすべてのキー、第3列は第2列で選択されたキーに対応する値です。

> キーに対応する値を変更したい場合は、toString関数をオーバーライドできます。


![_hive_img_01.png](/images/hive/_hive_img_01.png)

対応するコード

```javascript
    await DdCheckPlugin().init(dio, initHost: '192.168.100.64', port: 9998, projectName: 'shop', extend: [
      HiveToolManager(boxList: [MyCategoryCache()])
    ]);

```
DdPluginHiveBoxインターフェースを実装するだけでOKです。
```javascript
class MyCategoryCache extends DdPluginHiveBox<CategoryWrapper> {
  MyCategoryCache() : super("dd_category_box");

  @override
  Future<Box<CategoryWrapper>> get getBox => Hive.isBoxOpen(boxName) ? Future.value(Hive.box(boxName)) : Hive.openBox(boxName);
}
