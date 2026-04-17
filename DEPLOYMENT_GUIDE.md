# FlutterX 文档部署指南

当前站点使用 MkDocs，并通过 GitHub Actions 发布到 GitHub Pages。

## 项目结构

```text
flutterx-doc/
├── docs/
├── overrides/
├── mkdocs.yml
├── requirements.txt
└── .github/workflows/deploy.yml
```

## 自动部署

工作流文件是 `.github/workflows/deploy.yml`，在推送到 `main` 分支时自动执行。

主要步骤：

1. 检出仓库
2. 安装 Python
3. 安装 `requirements.txt` 依赖
4. 运行 `mkdocs build --clean --strict`
5. 上传 `site/`
6. 部署到 GitHub Pages

GitHub 仓库的 Pages 设置里，部署来源应选择 `GitHub Actions`。

## 本地验证

```bash
python -m pip install -r requirements.txt
mkdocs build --clean --strict
```

构建成功后，静态文件位于 `site/`。

## 手动触发部署

```bash
./deploy.sh
```

该脚本会先本地执行一次 MkDocs 构建，然后在安装了 GitHub CLI 的情况下触发远端工作流。

## 故障排查

如果部署失败，优先检查：

1. `mkdocs.yml` 配置是否有效
2. `requirements.txt` 依赖是否完整
3. GitHub Pages 是否配置为 `GitHub Actions`
4. Actions 日志中是否有严格模式构建错误

## 访问地址

[https://mdddj.github.io/flutterx-doc/](https://mdddj.github.io/flutterx-doc/)
