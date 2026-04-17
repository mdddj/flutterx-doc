# Riverpod Widget Tool


このツールは、StatelessWidgetをConsumerWidgetに自動変換できます。

また、StatefulWidgetをConsumerStatefulWidgetに自動変換することもできます。

> Riverpodの作者が`custom_lint`というプラグインパッケージを提供しており、同様の機能を実現できますが、このパッケージはバックグラウンドでDartアナライザーを起動し、メモリを極端に占有します（約2GBのメモリ）。メモリが豊富なユーザーはこの機能を無視できます。


<warning>
    <p>注意: この機能を使用するには、flutter_hooksパッケージを追加する必要があります。</p>
</warning>


####  機能プレビュー(StatelessWidget)

<video controls autoplay loop muted playsinline style="max-width: 100%; height: auto;" aria-label="Riverpod widget tool stateless demo" src="../../../assets/videos/gif/riverpod_1.mp4"></video>


####  機能プレビュー(StatefulWidget)

<video controls autoplay loop muted playsinline style="max-width: 100%; height: auto;" aria-label="Riverpod widget tool stateful demo" src="../../../assets/videos/gif/riverpod_2.mp4"></video>
