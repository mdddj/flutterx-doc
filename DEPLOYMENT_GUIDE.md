# FlutterX 文档部署指南

本文档详细说明如何将 FlutterX 文档项目部署到 GitHub Pages。

## 项目结构

FlutterX 文档项目是 git 仓库中的一个子目录，结构如下：

```
flutterx-doc/
├── docs/
├── doc_build/
├── .github/workflows/
├── package.json
├── rspress.config.ts
└── ...
```

## 自动部署

### GitHub Actions 工作流

项目包含一个 GitHub Actions 工作流文件 `.github/workflows/deploy-pages.yml`，它会在每次推送到 `main` 分支时自动触发部署。

工作流包含以下步骤：
1. 检出代码
2. 设置 Node.js 环境
3. 安装依赖
4. 构建文档
5. 上传构建产物
6. 部署到 GitHub Pages

### 配置要求

要使自动部署正常工作，需要在 GitHub 仓库设置中正确配置 GitHub Pages：

1. 访问仓库的 Settings 页面
2. 在左侧菜单中点击 "Pages"
3. 在 "Build and deployment" 部分：
   - Source: 选择 "GitHub Actions"
4. 保存设置

## 手动部署

### 使用部署脚本

项目包含一个 `deploy.sh` 脚本，可以手动触发部署：

```bash
./deploy.sh
```

该脚本会：
1. 运行 `npm run build` 构建文档
2. 如果安装了 GitHub CLI，会尝试触发 GitHub Actions 工作流
3. 如果未安装 GitHub CLI，会提供手动触发工作流的链接

### 手动构建和部署

如果需要手动构建和部署，可以按照以下步骤操作：

1. 构建文档：
   ```bash
   npm run build
   ```

2. 构建产物将位于 `doc_build/` 目录中

3. 可以手动将 `doc_build/` 目录的内容推送到 `gh-pages` 分支，或者通过 GitHub Actions 工作流进行部署

## 故障排除

### 工作流失败

如果 GitHub Actions 工作流失败，请检查以下几点：

1. 确保 `package.json` 中的构建脚本正确
2. 检查 `rspress.config.ts` 配置是否正确
3. 确认 GitHub Pages 设置正确
4. 查看工作流运行日志以获取详细错误信息

### GitHub Pages 未正确显示

如果 GitHub Pages 未正确显示文档，请检查以下几点：

1. 确保 GitHub Pages 设置中选择了正确的源（GitHub Actions）
2. 确认工作流成功完成
3. 检查自定义域名设置（如果使用）

## 访问部署的文档

部署成功后，可以通过以下链接访问文档：
[https://mdddj.github.io/flutterx-doc/](https://mdddj.github.io/flutterx-doc/)

## 相关文件

- `.github/workflows/deploy-pages.yml` - GitHub Actions 部署工作流
- `deploy.sh` - 手动部署脚本
- `package.json` - 项目依赖和脚本
- `rspress.config.ts` - Rspress 配置文件
- `README.md` - 项目说明文件
