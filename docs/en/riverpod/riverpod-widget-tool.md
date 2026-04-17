# Riverpod Widget Tool

This tool can automatically convert StatelessWidget to ConsumerWidget

It can also automatically convert StatefulWidget to ConsumerStatefulWidget

> Although the Riverpod author provides a plugin package `custom_lint` that can achieve similar functionality, this package will start a Dart analyzer in the background, consuming a lot of memory (about 2GB of memory). Users with large memory can ignore this feature.

<warning>
    <p>Note: You need to add the flutter_hooks package to use this feature</p>
</warning>

#### Feature Preview (StatelessWidget)

<video controls autoplay loop muted playsinline style="max-width: 100%; height: auto;" aria-label="Riverpod widget tool stateless demo" src="../../assets/videos/gif/riverpod_1.mp4"></video>

#### Feature Preview (StatefulWidget)

<video controls autoplay loop muted playsinline style="max-width: 100%; height: auto;" aria-label="Riverpod widget tool stateful demo" src="../../assets/videos/gif/riverpod_2.mp4"></video>
