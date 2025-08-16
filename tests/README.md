# FlutterX Documentation Test Suite

这是 FlutterX 文档迁移项目的综合测试套件，用于验证从 rspress 到 mkdocs-material 的迁移质量。

## 测试套件概览

### 🧪 测试类型

1. **内容迁移测试** (`test_content_migration.py`)

   - 验证目录结构完整性
   - 检查多语言目录存在性
   - 验证 Markdown 文件迁移
   - 检查资源文件迁移
   - 验证文件数量一致性
   - 检查内容保存完整性
   - 验证图片引用更新
   - 检查导航文件存在性

2. **多语言测试** (`test_multilanguage.py`)

   - 验证语言目录存在
   - 检查语言配置
   - 验证语言导航
   - 检查内容结构一致性
   - 验证语言切换器配置
   - 检查索引文件存在性
   - 验证跨语言一致性
   - 检查语言特定内容

3. **框架测试** (`test_framework.py`)

   - 验证 MkDocs 配置
   - 检查主题设置
   - 验证插件配置
   - 检查构建系统

4. **性能测试** (`test_performance.py`)

   - 测试构建时间
   - 检查站点大小
   - 验证内存使用
   - 测试脚本性能
   - 检查文件访问性能

5. **集成测试** (`test_integration.py`)
   - 完整迁移工作流测试
   - 构建和服务工作流测试
   - 验证工作流测试
   - 部署准备测试
   - 端到端工作流测试
   - 错误处理测试

## 🚀 运行测试

### 运行所有测试

```bash
python3 tests/run_all_tests.py
```

### 运行快速测试

```bash
python3 tests/run_all_tests.py --quick
```

### 运行单个测试套件

```bash
# 内容迁移测试
python3 tests/test_content_migration.py

# 多语言测试
python3 tests/test_multilanguage.py

# 框架测试
python3 tests/test_framework.py

# 性能测试
python3 tests/test_performance.py

# 集成测试
python3 tests/test_integration.py
```

### 生成测试总结

```bash
python3 tests/test_summary.py
```

## 📊 测试报告

测试运行后会生成以下报告文件：

- `test-summary.json` - JSON 格式的测试总结
- `test-summary.txt` - 文本格式的测试总结
- `content-migration-test-report.json` - 内容迁移测试详细报告
- `multilanguage-test-report.json` - 多语言测试详细报告
- `performance-report.txt` - 性能测试报告
- `integration-test-report.txt` - 集成测试报告
- `comprehensive-test-report.txt` - 综合测试报告

## 📈 当前测试状态

根据最新的测试运行结果：

- **总体成功率**: 93.8%
- **测试套件**: 2 个
- **总测试数**: 16 个
- **通过**: 15 个
- **失败**: 1 个

### 测试套件详情

1. **内容迁移测试**: 7/8 通过 (87.5%)

   - ❌ 内容保存测试失败（部分索引文件缺少标题）
   - ✅ 其他所有测试通过

2. **多语言测试**: 8/8 通过 (100.0%)
   - ✅ 所有多语言功能正常

## 🔧 测试配置

测试配置在 `test_config.py` 中定义，包括：

- 项目目录结构
- 支持的语言列表
- 文件模式和阈值
- 性能基准
- 必需文件和目录

## 🛠️ 故障排除

### 常见问题

1. **测试脚本不可执行**

   ```bash
   chmod +x tests/*.py
   ```

2. **缺少依赖**

   ```bash
   pip install -r requirements.txt
   ```

3. **权限问题**
   ```bash
   # 确保有读写权限
   chmod -R 755 mkdocs-flutterx/
   ```

### 调试测试失败

1. 查看详细的测试报告文件
2. 运行单个测试套件进行调试
3. 检查项目结构是否完整
4. 验证所有迁移脚本是否正确执行

## 📝 添加新测试

要添加新的测试：

1. 在相应的测试文件中添加测试方法
2. 使用统一的测试框架格式
3. 更新测试配置（如需要）
4. 运行测试验证功能
5. 更新文档

## 🎯 测试目标

这个测试套件的目标是确保：

- ✅ 所有内容正确迁移
- ✅ 多语言功能完整
- ✅ 构建系统正常工作
- ✅ 性能满足要求
- ✅ 部署准备就绪
- ✅ 错误处理健壮

## 📞 支持

如果遇到测试相关问题，请：

1. 检查测试报告文件
2. 查看项目文档
3. 验证环境配置
4. 联系开发团队

---

**注意**: 在部署到生产环境之前，请确保所有测试都通过，特别是集成测试和性能测试。
