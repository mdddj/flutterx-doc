#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
from pathlib import Path
import json

class FinalDocChecker:
    def __init__(self):
        self.docs_path = Path("flutterx-doc/docs")
        self.public_path = Path("flutterx-doc/docs/public")
        self.issues = []

    def check_image_links(self):
        """检查图片链接是否有效"""
        print("检查图片链接...")

        for md_file in self.docs_path.rglob("*.md"):
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # 查找所有图片引用
                img_matches = re.findall(r'!\[([^\]]*)\]\(([^)]+)\)', content)
                img_tag_matches = re.findall(r'<img[^>]+src="([^"]+)"', content)

                # 检查 markdown 图片
                for alt, src in img_matches:
                    if src.startswith('/'):
                        img_path = self.public_path / src.lstrip('/')
                        if not img_path.exists():
                            self.issues.append(f"缺失图片: {md_file} -> {src}")

                # 检查 img 标签
                for src in img_tag_matches:
                    if src.startswith('/'):
                        img_path = self.public_path / src.lstrip('/')
                        if not img_path.exists():
                            self.issues.append(f"缺失图片: {md_file} -> {src}")

            except Exception as e:
                self.issues.append(f"读取文件失败: {md_file} - {e}")

    def check_internal_links(self):
        """检查内部链接是否有效"""
        print("检查内部链接...")

        for md_file in self.docs_path.rglob("*.md"):
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # 查找内部链接（不包含 http 的链接）
                link_matches = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)

                for text, href in link_matches:
                    if not href.startswith(('http', 'mailto:', '#')):
                        # 假设是文档内部链接
                        if href.startswith('/'):
                            target_path = self.docs_path / href.lstrip('/')
                            if not target_path.with_suffix('.md').exists():
                                self.issues.append(f"断开的内部链接: {md_file} -> {href}")

            except Exception as e:
                self.issues.append(f"检查链接失败: {md_file} - {e}")

    def fix_common_issues(self):
        """修复常见问题"""
        print("修复常见问题...")

        fixed_files = 0

        for md_file in self.docs_path.rglob("*.md"):
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                original_content = content

                # 修复空链接
                content = re.sub(r'\[\]\(([^)]+)\)', r'[链接](\1)', content)

                # 修复重复的空行
                content = re.sub(r'\n{4,}', '\n\n\n', content)

                # 修复行尾空格
                content = re.sub(r' +\n', '\n', content)

                # 修复代码块语言标识
                content = re.sub(r'```Javascript', '```javascript', content)
                content = re.sub(r'```Dart', '```dart', content)
                content = re.sub(r'```Kotlin', '```kotlin', content)
                content = re.sub(r'```YAML', '```yaml', content)
                content = re.sub(r'```Bash', '```bash', content)

                # 修复引用块格式
                content = re.sub(r'>\s*\*\*([^*]+)\*\*\s*\n>\s*\n>', r'> **\1**\n>\n>', content)

                # 确保文档以换行符结尾
                if not content.endswith('\n'):
                    content += '\n'

                if original_content != content:
                    with open(md_file, 'w', encoding='utf-8') as f:
                        f.write(content)
                    fixed_files += 1
                    print(f"修复了: {md_file}")

            except Exception as e:
                self.issues.append(f"修复文件失败: {md_file} - {e}")

        print(f"共修复了 {fixed_files} 个文件")

    def validate_rspress_config(self):
        """验证 rspress 配置文件"""
        print("验证 rspress 配置...")

        config_path = Path("flutterx-doc/rspress.config.ts")
        if not config_path.exists():
            self.issues.append("rspress.config.ts 文件不存在")
            return

        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config_content = f.read()

            # 检查基本配置项
            required_configs = ['title', 'description', 'root', 'themeConfig']
            for config in required_configs:
                if config not in config_content:
                    self.issues.append(f"rspress 配置缺少: {config}")

        except Exception as e:
            self.issues.append(f"读取 rspress 配置失败: {e}")

    def generate_sitemap(self):
        """生成站点地图"""
        print("生成文档结构...")

        sitemap = {
            "文档结构": {},
            "统计信息": {
                "总文档数": 0,
                "总图片数": 0,
                "总视频数": 0,
                "总GIF数": 0
            }
        }

        # 统计文档
        for md_file in self.docs_path.rglob("*.md"):
            relative_path = md_file.relative_to(self.docs_path)
            sitemap["文档结构"][str(relative_path)] = {
                "大小": md_file.stat().st_size,
                "修改时间": md_file.stat().st_mtime
            }
            sitemap["统计信息"]["总文档数"] += 1

        # 统计资源
        if self.public_path.exists():
            for img_file in self.public_path.rglob("*.png"):
                sitemap["统计信息"]["总图片数"] += 1
            for img_file in self.public_path.rglob("*.jpg"):
                sitemap["统计信息"]["总图片数"] += 1
            for img_file in self.public_path.rglob("*.jpeg"):
                sitemap["统计信息"]["总图片数"] += 1
            for img_file in self.public_path.rglob("*.svg"):
                sitemap["统计信息"]["总图片数"] += 1
            for gif_file in self.public_path.rglob("*.gif"):
                sitemap["统计信息"]["总GIF数"] += 1
            for video_file in self.public_path.rglob("*.mp4"):
                sitemap["统计信息"]["总视频数"] += 1

        # 保存站点地图
        with open("flutterx-doc/docs_sitemap.json", 'w', encoding='utf-8') as f:
            json.dump(sitemap, f, ensure_ascii=False, indent=2)

        print(f"文档统计: {sitemap['统计信息']}")

    def create_missing_index_files(self):
        """创建缺失的 index 文件"""
        print("检查并创建缺失的 index 文件...")

        # 检查每个目录是否有对应的文档
        directories = [d for d in self.docs_path.iterdir() if d.is_dir() and d.name != 'public']

        for directory in directories:
            # 检查是否有同名的 .md 文件
            corresponding_md = self.docs_path / f"{directory.name}.md"
            index_md = directory / "index.md"

            if not corresponding_md.exists() and not index_md.exists():
                # 创建一个简单的 index 文件
                index_content = f"""# {directory.name}

这是 {directory.name} 相关功能的文档目录。

## 子页面

"""
                # 添加子页面链接
                for md_file in directory.rglob("*.md"):
                    if md_file.name != "index.md":
                        relative_path = md_file.relative_to(directory)
                        name = md_file.stem
                        index_content += f"- [{name}](./{relative_path.with_suffix('').as_posix()})\n"

                with open(index_md, 'w', encoding='utf-8') as f:
                    f.write(index_content)

                print(f"创建了索引文件: {index_md}")

    def run(self):
        """运行完整检查"""
        print("开始最终文档检查和优化...")
        print("=" * 50)

        # 执行各项检查和修复
        self.check_image_links()
        self.check_internal_links()
        self.fix_common_issues()
        self.validate_rspress_config()
        self.generate_sitemap()
        self.create_missing_index_files()

        # 输出结果
        print("\n" + "=" * 50)
        print("检查结果:")

        if self.issues:
            print(f"发现 {len(self.issues)} 个问题:")
            for issue in self.issues:
                print(f"  ❌ {issue}")
        else:
            print("✅ 没有发现问题")

        print("\n优化建议:")
        print("1. 定期运行此脚本检查文档完整性")
        print("2. 确保所有图片都有合适的 alt 文本")
        print("3. 保持文档结构清晰，避免过深的嵌套")
        print("4. 定期更新过时的链接和内容")

        print("\n文档迁移完成！")
        print("你可以运行以下命令启动 rspress 开发服务器:")
        print("cd flutterx-doc && npm run dev")

if __name__ == "__main__":
    checker = FinalDocChecker()
    checker.run()
