# FlutterX 插件文档

FlutterX 是一个为 Flutter 开发者提供快速开发辅助工具的插件。

## 文档网站

文档已通过 GitHub Actions 部署到 GitHub Pages，可以通过以下链接访问：

[https://mdddj.github.io/flutterx-doc/](https://mdddj.github.io/flutterx-doc/)

## 本地开发

### 安装依赖
```bash
npm install
```

### 启动开发服务器
```bash
npm run dev
```

### 构建文档
```bash
npm run build
```

## 部署

文档通过 GitHub Actions 自动部署到 GitHub Pages。每次推送到 `main` 分支时都会触发部署流程。

### 手动部署

您也可以使用提供的部署脚本来手动触发部署：

```bash
./deploy.sh
```

### 手动设置 GitHub Pages（如果自动部署失败）

如果 GitHub Actions 部署失败，您可以手动设置 GitHub Pages：

1. 访问仓库的 Settings 页面
2. 在左侧菜单中点击 "Pages"
3. 在 "Build and deployment" 部分：
   - Source: 选择 "GitHub Actions"
4. 保存设置

部署成功后，您可以通过以下链接访问文档：
[https://mdddj.github.io/flutterx-doc/](https://mdddj.github.io/flutterx-doc/)
