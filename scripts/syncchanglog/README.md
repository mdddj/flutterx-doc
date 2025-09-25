# syncchanglog 使用说明

本工具用于从指定 URL 下载 Markdown 文件，并将其保存到一个或多个本地路径。你可以通过命令行参数或配置文件来配置它。

## 1. 编译项目

在终端中进入 `scripts/syncchanglog` 目录，然后运行以下命令来构建发布版本的可执行文件：

```sh
cargo build --release
```

编译后的二进制文件将位于 `target/release/syncchanglog`。

## 2. 如何运行

你可以通过以下几种方式运行本工具：

### A) 直接使用命令行参数

直接在命令行中提供 URL 和输出路径。

```sh
./target/release/syncchanglog \
    --url "https://raw.githubusercontent.com/user/repo/main/CHANGELOG.md" \
    --outputs ./CHANGELOG.md ../../docs/CHANGELOG.md
```

### B) 使用 JSON 配置文件

创建一个配置文件（例如 `config.json`）：

```json
{
  "url": "https://raw.githubusercontent.com/user/repo/main/CHANGELOG.md",
  "outputs": [
    "./CHANGELOG.md",
    "../../docs/CHANGELOG.md"
  ]
}
```

然后，使用 `--config` 标志运行工具：

```sh
./target/release/syncchanglog --config ./config.json
```

### C) 使用 YAML 配置文件

或者，创建一个 YAML 文件（例如 `config.yaml`）：

```yaml
url: "https://raw.githubusercontent.com/user/repo/main/CHANGELOG.md"
outputs:
  - "./CHANGELOG.md"
  - "../../docs/CHANGELOG.md"
```

然后运行工具：

```sh
./target/release/syncchanglog --config ./config.yaml
```

### D) 混合使用（参数会覆盖配置）

你可以将配置文件与命令行参数结合使用。命令行参数的优先级总是高于配置文件中的值。

例如，你可以使用 `config.yaml` 文件中定义的 `outputs`，同时在命令行中指定一个不同的 URL：

```sh
./target/release/syncchanglog \
    --config ./config.yaml \
    --url "https://raw.githubusercontent.com/another-user/another-repo/dev/CHANGELOG.md"
```
