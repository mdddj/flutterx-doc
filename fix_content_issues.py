#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
from pathlib import Path
import xml.etree.ElementTree as ET

class ContentIssuesFixer:
    def __init__(self):
        self.docs_path = Path("flutterx-doc/docs")
        self.writerside_path = Path("Writerside")

    def fix_installation_doc(self):
        """修复安装文档的内容问题"""
        install_path = self.docs_path / "安装.md"

        content = """# 开始使用

[FlutterX](https://flutterx.itbug.shop) 是一个Flutter开发者快速开发的辅助工具插件,支持dio请求监听,json快速生成freezed对象,Hive可视化查看对象,shared_preferences可视化浏览等等强大功能

> **注意**
>
> 它是开源且免费的,由**梁典典**开发维护,如果你想查看源码,请查看[Github](https://github.com/mdddj/dd_flutter_idea_plugin)

## 在idea市场安装

1. 打开idea插件市场搜索`flutterx`,第一个就是
2. ![flutterx](/images/start/start_01.png)

## 编译源码

> **注意**
>
> 插件使用Kotlin语言编写,gradle构建

1. 拉取源码

```bash
git clone https://github.com/mdddj/dd_flutter_idea_plugin
```

2. 拉取依赖

```bash
cd dd_flutter_idea_plugin && ./gradlew -i --info
```

3. 打包

```bash
./gradlew buildPlugin --info
```

## 编译其他idea版本,AS版本

查看要编译版本对应的版本号，修改对应的`sinceBuildVersion`和`untilBuildVersion`,重新构建就好了

> **警告**
>
> 修改后可能要进行JBR适配

```kotlin
kotlin.stdlib.default.dependency=true
kotlin.incremental.useClasspathSnapshot=false
kotlin.experimental.tryK2=true
kapt.use.k2=true
pluginVersion=4.0.1
#===============================> 223 AS release version : https://plugins.jetbrains.com/docs/intellij/android-studio-releases-list.html
#===============================> 正式版本最新 Giraffe
#dartVersion=223.8977
#flutterVersion=76.3.2
#sinceBuildVersion=223
#untilBuildVersion=223.*
#ideaVersion=2022.3.1.18
#ideaType=AI
#===============================> 231 AS Hedgehog version : https://plugins.jetbrains.com/docs/intellij/android-studio-releases-list.html
#dartVersion=231.9402
#flutterVersion=76.3.3
#sinceBuildVersion=231
#untilBuildVersion=231.*
#ideaVersion=2023.1.1.24
#ideaType=AI
#===============================> 232 AS   Iguana
#dartVersion=232.10248
#flutterVersion=76.3.4
#sinceBuildVersion=232
#untilBuildVersion=232.*
#ideaVersion=2023.2.1.11
#ideaType=AI
#===============================> 233 idea IU  2023.3
dartVersion=233.11799.172
flutterVersion=77.0.1
sinceBuildVersion=233
untilBuildVersion=233.*
ideaVersion=2023.3
ideaType=IU
#===============================================
```

"""

        with open(install_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"修复了安装文档: {install_path}")

    def fix_code_language_tags(self, content):
        """修复代码块语言标签"""
        # Dart 代码应该使用 dart 而不是 javascript
        content = re.sub(r'```javascript\s*\n(\s*void main\(\))', r'```dart\n\1', content)
        content = re.sub(r'```javascript\s*\n(\s*DdCheckPlugin)', r'```dart\n\1', content)
        content = re.sub(r'```javascript\s*\n(\s*SendResponseModel)', r'```dart\n\1', content)

        return content

    def fix_table_formatting(self, content):
        """修复表格格式"""
        lines = content.split('\n')
        fixed_lines = []
        in_table = False

        for i, line in enumerate(lines):
            # 检测表格开始
            if '|' in line and not in_table:
                # 确保表格前有空行
                if fixed_lines and fixed_lines[-1].strip():
                    fixed_lines.append('')
                in_table = True
                fixed_lines.append(line)

                # 检查是否需要添加表格分隔行
                if i + 1 < len(lines) and '|' in lines[i + 1] and not lines[i + 1].startswith('|---'):
                    # 计算列数
                    col_count = line.count('|') - 1
                    separator = '|' + '---|' * col_count
                    fixed_lines.append(separator)

            elif '|' in line and in_table:
                fixed_lines.append(line)
            elif in_table and not '|' in line:
                # 表格结束
                in_table = False
                # 确保表格后有空行
                if line.strip():
                    fixed_lines.append('')
                fixed_lines.append(line)
            else:
                fixed_lines.append(line)

        return '\n'.join(fixed_lines)

    def fix_note_blocks(self, content):
        """修复提示块格式"""
        # 修复注意块
        content = re.sub(r'> 注意,需要 FlutterX版本([^\\n]+)', r'> **注意**\n>\n> 需要 FlutterX版本\1', content)

        # 修复其他提示块
        content = re.sub(r'> 简单解释一下', r'> **说明**\n>\n> 简单解释一下', content)

        return content

    def fix_link_formatting(self, content):
        """修复链接格式"""
        # 修复空链接
        content = re.sub(r'\[([^\]]+)\]\(\)', r'[\1](https://pub.dev/packages/freezed)', content)

        return content

    def process_all_files(self):
        """处理所有文档文件"""
        print("开始修复内容问题...")

        # 首先修复安装文档
        self.fix_installation_doc()

        fixed_count = 0

        # 处理所有 markdown 文件
        for md_file in self.docs_path.rglob("*.md"):
            if md_file.name == "安装.md":
                continue  # 已经单独处理过了

            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                original_content = content

                # 应用各种修复
                content = self.fix_code_language_tags(content)
                content = self.fix_table_formatting(content)
                content = self.fix_note_blocks(content)
                content = self.fix_link_formatting(content)

                if original_content != content:
                    with open(md_file, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"修复了内容问题: {md_file}")
                    fixed_count += 1

            except Exception as e:
                print(f"处理文件 {md_file} 时出错: {e}")

        print(f"完成！共修复了 {fixed_count + 1} 个文件的内容问题。")

    def organize_docs_structure(self):
        """整理文档结构，将根目录的文档移动到合适的目录"""

        # 需要移动的文件映射
        move_mapping = {
            "Project-Library-scan.md": "dart-file/",
            "generate.md": "freezed/",
            "不再更新的三方包检测.md": "pubspec/",
            "flutter3-29-0安卓迁移gradle工具.md": "other/",
            "freezed-3-x版本迁移工具.md": "freezed/",
            "Json-to-Freezed.md": "freezed/",
            "资产文件路径检查功能.md": "dart-file/",
            "l10n-editor.md": "other/",
            "Log.md": "other/"
        }

        for filename, target_dir in move_mapping.items():
            source_path = self.docs_path / filename
            target_path = self.docs_path / target_dir / filename

            if source_path.exists():
                # 确保目标目录存在
                target_path.parent.mkdir(parents=True, exist_ok=True)

                # 如果目标文件已存在，删除源文件
                if target_path.exists():
                    source_path.unlink()
                    print(f"删除重复文件: {source_path}")
                else:
                    # 移动文件
                    source_path.rename(target_path)
                    print(f"移动文件: {source_path} -> {target_path}")

    def run(self):
        """运行修复程序"""
        self.organize_docs_structure()
        self.process_all_files()

if __name__ == "__main__":
    fixer = ContentIssuesFixer()
    fixer.run()
