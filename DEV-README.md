# FlutterX Documentation Development Guide

这是 FlutterX 文档项目的开发环境指南，包含了所有开发、构建和部署所需的工具和脚本。

## 🚀 快速开始

### 1. 环境准备

```bash
# 安装依赖
pip install -r requirements.txt

# 安装可选的开发依赖
pip install watchdog  # 用于文件监控和热重载
```

### 2. 开发服务器

```bash
# 启动开发服务器（推荐）
python dev.py serve

# 或者直接使用脚本
python scripts/dev-server.py

# 自定义端口和主机
python dev.py serve --port 8080 --host 0.0.0.0

# 禁用自动打开浏览器
python dev.py serve --no-browser
```

### 3. 构建站点

```bash
# 开发构建
python dev.py build

# 生产构建（包含优化）
python dev.py build --production

# 跳过测试的快速构建
python dev.py build --no-tests
```

## 📁 项目结构

```
mkdocs-flutterx/
├── docs/                    # 文档内容
│   ├── zh/                 # 中文文档
│   ├── en/                 # 英文文档
│   ├── ja/                 # 日文文档
│   └── assets/             # 资源文件
├── scripts/                # 开发脚本
│   ├── dev-server.py       # 开发服务器
│   ├── build-automation.py # 构建自动化
│   ├── production-build.py # 生产构建
│   ├── hot-reload.py       # 热重载服务器
│   └── ...                 # 其他脚本
├── tests/                  # 测试套件
├── overrides/              # 主题覆盖
├── site/                   # 构建输出（自动生成）
├── mkdocs.yml             # MkDocs配置
├── dev-config.json        # 开发配置
├── dev.py                 # 开发管理器
└── requirements.txt       # Python依赖
```

## 🛠️ 开发工具

### 开发管理器 (`dev.py`)

这是主要的开发工具，提供了统一的命令接口：

```bash
# 查看所有可用命令
python dev.py help

# 查看项目状态
python dev.py status

# 启动开发服务器
python dev.py serve

# 构建站点
python dev.py build

# 运行测试
python dev.py test

# 运行迁移
python dev.py migrate

# 验证内容
python dev.py validate

# 清理构建文件
python dev.py clean
```

### 开发服务器 (`scripts/dev-server.py`)

功能特性：

- 自动重载
- 浏览器自动打开
- 端口冲突检测
- 实时日志输出

```bash
# 基本使用
python scripts/dev-server.py

# 自定义配置
python scripts/dev-server.py --port 8080 --host 0.0.0.0 --no-browser

# 仅构建不启动服务器
python scripts/dev-server.py --build-only

# 文件监控模式
python scripts/dev-server.py --watch
```

### 热重载服务器 (`scripts/hot-reload.py`)

高级文件监控和自动重载：

```bash
# 启动热重载服务器
python scripts/hot-reload.py

# 自定义配置
python scripts/hot-reload.py --port 8080 --no-browser
```

### 构建自动化 (`scripts/build-automation.py`)

自动化构建流程：

```bash
# 完整构建流程
python scripts/build-automation.py

# 跳过测试
python scripts/build-automation.py --no-tests

# 跳过优化
python scripts/build-automation.py --no-optimize

# 启用压缩
python scripts/build-automation.py --compress
```

### 生产构建 (`scripts/production-build.py`)

生产环境优化构建：

```bash
# 完整生产构建
python scripts/production-build.py

# 跳过特定优化
python scripts/production-build.py --no-minify --no-gzip --no-hash
```

## 🧪 测试

### 运行测试

```bash
# 运行所有测试
python dev.py test

# 运行快速测试
python dev.py test --quick

# 运行特定测试套件
python dev.py test --suite content_migration
python dev.py test --suite multilanguage
python dev.py test --suite framework
```

### 测试套件

1. **内容迁移测试** - 验证内容迁移完整性
2. **多语言测试** - 验证多语言功能
3. **框架测试** - 验证 MkDocs 配置
4. **性能测试** - 验证构建性能
5. **集成测试** - 端到端测试

## 🔧 配置

### 开发配置 (`dev-config.json`)

```json
{
  "development": {
    "server": {
      "host": "127.0.0.1",
      "port": 8000,
      "auto_open_browser": true,
      "live_reload": true
    },
    "watch": {
      "patterns": ["*.md", "*.yml", "*.css", "*.js"],
      "ignore_patterns": ["site/*", "*.pyc"],
      "reload_delay": 1.0
    }
  },
  "production": {
    "build": {
      "minify_html": true,
      "minify_css": true,
      "optimize_images": true,
      "generate_gzip": true
    }
  }
}
```

### 热重载配置 (`hot-reload-config.json`)

```json
{
  "watch_patterns": ["*.md", "*.yml", "*.css", "*.js"],
  "ignore_patterns": ["site/*", "*.pyc"],
  "watch_directories": ["docs", "overrides"],
  "reload_delay": 1.0,
  "server_port": 8000
}
```

## 📝 开发工作流

### 日常开发

1. **启动开发环境**

   ```bash
   python dev.py serve
   ```

2. **编辑文档**

   - 修改 `docs/` 目录下的 Markdown 文件
   - 自动重载会实时显示更改

3. **测试更改**

   ```bash
   python dev.py test --quick
   ```

4. **构建验证**
   ```bash
   python dev.py build
   ```

### 发布准备

1. **运行完整测试**

   ```bash
   python dev.py test
   ```

2. **内容验证**

   ```bash
   python dev.py validate
   ```

3. **生产构建**

   ```bash
   python dev.py build --production
   ```

4. **部署准备**
   ```bash
   python scripts/prepare-deployment.py
   ```

## 🚨 故障排除

### 常见问题

1. **端口被占用**

   ```bash
   # 使用不同端口
   python dev.py serve --port 8080
   ```

2. **依赖缺失**

   ```bash
   pip install -r requirements.txt
   pip install watchdog  # 可选
   ```

3. **权限问题**

   ```bash
   chmod +x scripts/*.py
   chmod +x dev.py
   ```

4. **构建失败**
   ```bash
   # 清理并重新构建
   python dev.py clean --all
   python dev.py build
   ```

### 调试模式

```bash
# 启用详细日志
export MKDOCS_VERBOSE=1
python dev.py serve

# 检查项目状态
python dev.py status

# 运行诊断
python scripts/validate-content-comprehensive.py
```

## 📊 性能优化

### 开发环境优化

- 使用热重载减少重启时间
- 配置文件监控忽略不必要的文件
- 使用增量构建

### 生产构建优化

- HTML/CSS/JS 压缩
- 图片优化
- Gzip 压缩
- 缓存破坏（文件哈希）
- 静态资源优化

## 🔗 相关链接

- [MkDocs 官方文档](https://www.mkdocs.org/)
- [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)
- [项目测试报告](./test-summary.txt)
- [构建报告](./build-report.json)

## 💡 提示和技巧

1. **使用开发管理器** - `dev.py` 提供了统一的命令接口
2. **配置热重载** - 提高开发效率
3. **定期运行测试** - 确保代码质量
4. **使用生产构建** - 部署前进行优化
5. **监控构建性能** - 关注构建时间和输出大小

---

**注意**: 这个开发环境是为 FlutterX 文档项目特别设计的，包含了多语言支持、自动化测试和优化构建等功能。
