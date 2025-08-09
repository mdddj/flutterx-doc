# Hive Cache Viewing Tool

## 1. Getting Started

You need to add the `dd_check_plugin` dependency to your project and initialize the connection at an appropriate location.

```dart
    void main(){
    DdCheckPlugin().init(Dio(),
        initHost: "192.168.100.63", // Replace with your computer's IP
        port: 9999, // Plugin listening port
        projectName: 'App Name',
        extend: [
            HiveToolManager(boxList: [
              // Add the key code here, need to implement DdPluginHiveBox abstract class
            ])
    ]);
}
```

Definition of the `DdPluginHiveBox` class:

```javascript
abstract class DdPluginHiveBox<T> {
  final String boxName;

  DdPluginHiveBox(this.boxName);

  Future<Box<T>> get getBox;
}
```

> Here's an explanation of why you need to manually implement a `getBox` function: because when Hive opens a box, if no T generic is passed by default, it defaults to a dynamic type, which will cause Hive to report an error.

| Property | Description |
|----------|-------------|
| boxName  | Your Hive box name |
| getBox   | Returns the box object |

## 2. Usage Example

The panel has 3 columns: the first column is the box list, the second column shows all keys in the selected box from the first column, and the third column shows the value corresponding to the selected key from the second column.

> If you want to change the value corresponding to a key, you can override its toString function.

![_hive_img_01.png](/images/hive/_hive_img_01.png)

Corresponding code:

```javascript
    await DdCheckPlugin().init(dio, initHost: '192.168.100.64', port: 9998, projectName: 'shop', extend: [
      HiveToolManager(boxList: [MyCategoryCache()])
    ]);
```

Just implement the DdPluginHiveBox interface:

```javascript
class MyCategoryCache extends DdPluginHiveBox<CategoryWrapper> {
  MyCategoryCache() : super("dd_category_box");

  @override
  Future<Box<CategoryWrapper>> get getBox => Hive.isBoxOpen(boxName) ? Future.value(Hive.box(boxName)) : Hive.openBox(boxName);
}
```
