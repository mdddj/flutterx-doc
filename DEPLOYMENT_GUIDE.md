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

## Docker 部署

当前仓库也支持直接构建 Docker 镜像。镜像构建阶段会自动执行 MkDocs 构建，因此服务器不需要预先生成 `site/`。

### 构建参数

- `SITE_URL`: 文档站完整地址，决定 canonical 和 sitemap
- `ALT_LINK_ZH`
- `ALT_LINK_EN`
- `ALT_LINK_JA`

自定义域名示例：

```bash
docker build \
  --build-arg SITE_URL="https://docs.example.com/" \
  --build-arg ALT_LINK_ZH="/zh/" \
  --build-arg ALT_LINK_EN="/en/" \
  --build-arg ALT_LINK_JA="/ja/" \
  -t flutterx-doc:latest .
```

子路径部署示例：

```bash
docker build \
  --build-arg SITE_URL="https://example.com/flutterx-doc/" \
  --build-arg ALT_LINK_ZH="/flutterx-doc/zh/" \
  --build-arg ALT_LINK_EN="/flutterx-doc/en/" \
  --build-arg ALT_LINK_JA="/flutterx-doc/ja/" \
  -t flutterx-doc:latest .
```

### 运行

```bash
docker run -d \
  --name flutterx-doc \
  --restart unless-stopped \
  -p 8083:80 \
  flutterx-doc:latest
```

### Compose 和反向代理

- Compose 示例: `docker-compose.example.yml`
- Nginx 反向代理示例: `deploy/nginx-proxy.example.conf`

## GitHub Actions 自动推送 GHCR

工作流文件：

```text
.github/workflows/docker-image.yml
```

它会在推送到 `main` 时自动构建 Docker 镜像并推送到：

```text
ghcr.io/mdddj/flutterx-doc:latest
```

### 需要配置的 GitHub Variables

在仓库的 `Settings -> Secrets and variables -> Actions -> Variables` 中添加：

- `DOCKER_SITE_URL`
- `DOCKER_ALT_LINK_ZH`
- `DOCKER_ALT_LINK_EN`
- `DOCKER_ALT_LINK_JA`

自定义域名示例：

```text
DOCKER_SITE_URL=https://docs.example.com/
DOCKER_ALT_LINK_ZH=/zh/
DOCKER_ALT_LINK_EN=/en/
DOCKER_ALT_LINK_JA=/ja/
```

子路径部署示例：

```text
DOCKER_SITE_URL=https://example.com/flutterx-doc/
DOCKER_ALT_LINK_ZH=/flutterx-doc/zh/
DOCKER_ALT_LINK_EN=/flutterx-doc/en/
DOCKER_ALT_LINK_JA=/flutterx-doc/ja/
```

### 服务器拉取配置

直接使用 `docker-compose.ghcr.example.yml`：

```bash
docker compose pull
docker compose up -d
```

如果 GHCR 包是私有的，先在服务器登录：

```bash
echo "<github_pat>" | docker login ghcr.io -u <github_username> --password-stdin
```
