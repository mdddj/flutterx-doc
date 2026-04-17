# FlutterX 插件文档

这是 FlutterX 的 MkDocs 文档站点。

## 在线访问

文档通过 GitHub Actions 部署到 GitHub Pages：

[https://mdddj.github.io/flutterx-doc/](https://mdddj.github.io/flutterx-doc/)

## 本地开发

### 安装依赖

```bash
python -m pip install -r requirements.txt
```

### 启动开发服务器

```bash
mkdocs serve
```

### 构建文档

```bash
mkdocs build --clean --strict
```

构建产物默认输出到 `site/`。

如果需要兼容不同部署根地址，可以在构建时覆盖这些环境变量：

```bash
SITE_URL="https://mdddj.github.io/flutterx-doc/" \
ALT_LINK_ZH="/flutterx-doc/zh/" \
ALT_LINK_EN="/flutterx-doc/en/" \
ALT_LINK_JA="/flutterx-doc/ja/" \
mkdocs build --clean --strict
```

自定义域名部署时改成：

```bash
SITE_URL="https://flutterx.itbug.shop/" \
ALT_LINK_ZH="/zh/" \
ALT_LINK_EN="/en/" \
ALT_LINK_JA="/ja/" \
mkdocs build --clean --strict
```

## 部署

推送到 `main` 分支后，GitHub Actions 会自动构建并发布到 GitHub Pages。

如果需要手动触发部署，可以运行：

```bash
./deploy.sh
```

GitHub Pages 仓库设置中应选择 `GitHub Actions` 作为部署来源。
