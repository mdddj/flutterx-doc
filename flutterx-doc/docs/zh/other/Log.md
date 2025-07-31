# Log


## Log Window

> **注意**
>


有一些数据在控制台看起来不直观，也不方便，所以做了这个日志面板


![image_32.png](/images/image_32.png)


## 怎么用?


在你的项目中导入 [dd_check_plugin(v4.0.0+)](https://pub.dev/packages/dd_check_plugin) 这个包


连接到FlutterX插件


```dart

            DdCheckPlugin().init(Dio(),
                    initHost: "192.168.199.1", // 切换到你的局域网ip
                    port: 9999, // socket 端口，默认 9999
                    connectSuccess: (socket,SocketConnect connect) {
                // FlutterX 连接成功回调
            }, connectDisconnected: (connect) {
                //断开连接回调
            }, extend: [
                HiveToolManager(boxList: [DevCache.instance, AppMapCache(), UserCache()])
            ]);

```


连接 idea插件成功后，会返回一个 `SocketConnect` 对象，这个对象封装了一些函数，可以对 FlutterX进行一些操作


把 SocketConnect 示例存起来，然后调用这个发送日志函数


```dart

            connect.sendJsonLog(
                "测试日志", //标题
                {"hello":"world"}, // 数据
                subTitle: "sub title", // 副标题
                type: FlutterXLogType.info // 图标
            );

```


## 使用自带封装的函数发送日志


dd_check_plugin 封装了一个连接实例管理类，可以直接使用


```dart

            FlutterXConnectManager.instance.getFirstConnect()?.sendJsonLog("测试日志${DateTime.now().toIso8601String()}", {
                "hello":"world",
                "bool":true
              },type: FlutterXLogType.success);

```


