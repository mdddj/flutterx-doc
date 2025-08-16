# Riverpod Widget Tool

This tool can automatically convert StatelessWidget to ConsumerWidget

It can also automatically convert StatefulWidget to ConsumerStatefulWidget

> Although the Riverpod author provides a plugin package `custom_lint` that can achieve similar functionality, this package will start a Dart analyzer in the background, consuming a lot of memory (about 2GB of memory). Users with large memory can ignore this feature.

<warning>
    <p>Note: You need to add the flutter_hooks package to use this feature</p>
</warning>

#### Feature Preview (StatelessWidget)

![riverpod_1.gif](../../assets/gif/riverpod_1.gif)

#### Feature Preview (StatefulWidget)

![riverpod_2.gif](../../assets/gif/riverpod_2.gif)