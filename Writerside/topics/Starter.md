# Dio接口监听

## 1.窗口预览
如果找不到这个窗口,可能是默认没有显示,需要在菜单栏中手动打开: <shortcut>View -> Tool Windows -> Dio Request</shortcut>

![dio windows](img.png)

## 2.服务运行状态

如果出现小绿点,标识服务正在运行,可以开始连接使用了

![status](img_2.png)

## 3.开始使用

#### 添加依赖

```yaml
 dd_check_plugin: ^lastVersion
```

#### 拉取依赖
```Bash
flutter pub get
```

#### 编写代码

把你的 Dio 单例类传进去,插件会添加一个拦截器监听请求,然后把请求模型发送到 FlutterX插件端.


<code-block lang="dart">
    void main(){
    DdCheckPlugin().init(Dio(),
        initHost: "192.168.100.63",
        port: 9999,
        projectName: 'Flutter Shop2',);
}
</code-block>
