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

## Docker 部署

仓库内置了源码构建镜像的 Docker 方案，构建时会自动执行 `mkdocs build --clean --strict`。

### 直接构建

自定义域名部署：

```bash
docker build \
  --build-arg SITE_URL="https://docs.example.com/" \
  --build-arg ALT_LINK_ZH="/zh/" \
  --build-arg ALT_LINK_EN="/en/" \
  --build-arg ALT_LINK_JA="/ja/" \
  -t flutterx-doc:latest .
```

部署到子路径，例如 `https://example.com/flutterx-doc/`：

```bash
docker build \
  --build-arg SITE_URL="https://example.com/flutterx-doc/" \
  --build-arg ALT_LINK_ZH="/flutterx-doc/zh/" \
  --build-arg ALT_LINK_EN="/flutterx-doc/en/" \
  --build-arg ALT_LINK_JA="/flutterx-doc/ja/" \
  -t flutterx-doc:latest .
```

运行：

```bash
docker run -d \
  --name flutterx-doc \
  --restart unless-stopped \
  -p 8083:80 \
  flutterx-doc:latest
```

### Compose

可以直接复制 [`docker-compose.example.yml`](/Users/ldd/WritersideProjects/flutterx/docker-compose.example.yml) 为 `docker-compose.yml` 后修改域名参数，再执行：

```bash
docker compose up -d --build
```

如果服务器前面还有 Nginx，反向代理示例见 [`deploy/nginx-proxy.example.conf`](/Users/ldd/WritersideProjects/flutterx/deploy/nginx-proxy.example.conf)。

### GitHub Actions 自动推送 GHCR

仓库还内置了 [`.github/workflows/docker-image.yml`](/Users/ldd/WritersideProjects/flutterx/.github/workflows/docker-image.yml)，会在推送到 `main` 时自动构建并推送到：

```text
ghcr.io/mdddj/flutterx-doc:latest
```

在 GitHub 仓库 `Settings -> Secrets and variables -> Actions -> Variables` 里配置这些变量：

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

服务器如果直接拉 GHCR 镜像，可以复制 [`docker-compose.ghcr.example.yml`](/Users/ldd/WritersideProjects/flutterx/docker-compose.ghcr.example.yml) 为 `docker-compose.yml` 后执行：

```bash
docker compose pull
docker compose up -d
```
