# Log Tools

## Log Window

> **Note**
>

Some data in the console doesn't look intuitive and is not convenient, so this log panel was created.

![image_32.png](/images/image_32.png)

## How to use?

Import the [dd_check_plugin(v4.0.0+)](https://pub.dev/packages/dd_check_plugin) package in your project

Connect to the FlutterX plugin

```dart
DdCheckPlugin().init(Dio(),
        initHost: "192.168.199.1", // Switch to your LAN IP
        port: 9999, // Socket port, default 9999
        connectSuccess: (socket,SocketConnect connect) {
    // FlutterX connection success callback
}, connectDisconnected: (connect) {
    // Disconnection callback
}, extend: [
    HiveToolManager(boxList: [DevCache.instance, AppMapCache(), UserCache()])
]);
```

After successfully connecting to the IDE plugin, it will return a `SocketConnect` object. This object encapsulates some functions that can perform operations on FlutterX.

Store the SocketConnect instance and then call this log sending function

```dart
connect.sendJsonLog(
    "Test log", // Title
    {"hello":"world"}, // Data
    subTitle: "sub title", // Subtitle
    type: FlutterXLogType.info // Icon
);
```

## Using the built-in encapsulated function to send logs

dd_check_plugin encapsulates a connection instance management class that can be used directly

```dart
FlutterXConnectManager.instance.getFirstConnect()?.sendJsonLog("Test log ${DateTime.now().toIso8601String()}", {
    "hello":"world",
    "bool":true
  },type: FlutterXLogType.success);
```
