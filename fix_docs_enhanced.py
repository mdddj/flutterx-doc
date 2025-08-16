#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import shutil
from pathlib import Path
import xml.etree.ElementTree as ET

class EnhancedDocFixer:
    def __init__(self):
        self.docs_path = Path("flutterx-doc/docs")
        self.public_path = Path("flutterx-doc/docs/public")
        self.writerside_path = Path("Writerside")

    def copy_missing_resources(self):
        """复制缺失的资源文件"""
        print("检查和复制缺失的资源文件...")

        # 复制图片
        writerside_images = self.writerside_path / "images"
        target_images = self.public_path / "images"

        if writerside_images.exists():
            for img_file in writerside_images.rglob("*"):
                if img_file.is_file():
                    relative_path = img_file.relative_to(writerside_images)
                    target_file = target_images / relative_path

                    if not target_file.exists():
                        target_file.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(img_file, target_file)
                        print(f"复制图片: {img_file} -> {target_file}")

        # 复制GIF文件
        writerside_gifs = self.writerside_path / "gif"
        target_gifs = self.public_path / "gif"

        if writerside_gifs.exists():
            for gif_file in writerside_gifs.rglob("*"):
                if gif_file.is_file():
                    relative_path = gif_file.relative_to(writerside_gifs)
                    target_file = target_gifs / relative_path

                    if not target_file.exists():
                        target_file.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(gif_file, target_file)
                        print(f"复制GIF: {gif_file} -> {target_file}")

        # 复制视频文件
        writerside_videos = self.writerside_path / "videos"
        target_videos = self.public_path / "videos"

        if writerside_videos.exists():
            for video_file in writerside_videos.rglob("*"):
                if video_file.is_file():
                    relative_path = video_file.relative_to(writerside_videos)
                    target_file = target_videos / relative_path

                    if not target_file.exists():
                        target_file.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(video_file, target_file)
                        print(f"复制视频: {video_file} -> {target_file}")

    def find_actual_resource_path(self, resource_name, resource_type="images"):
        """在资源目录中查找实际的资源路径"""
        resource_dir = self.public_path / resource_type

        # 移除开头的下划线（如果有）
        clean_name = resource_name.lstrip('_')

        # 在所有子目录中搜索资源
        for root, dirs, files in os.walk(resource_dir):
            for file in files:
                if file == resource_name or file == clean_name:
                    # 返回相对于 public 目录的路径
                    relative_path = os.path.relpath(os.path.join(root, file), self.public_path)
                    return f"/{relative_path}"

        # 如果找不到，尝试搜索类似的文件名
        for root, dirs, files in os.walk(resource_dir):
            for file in files:
                if clean_name in file or file in clean_name:
                    relative_path = os.path.relpath(os.path.join(root, file), self.public_path)
                    return f"/{relative_path}"

        # 如果仍然找不到，返回默认路径
        return f"/{resource_type}/{resource_name}"

    def fix_writerside_syntax(self, content):
        """修复 Writerside 特有的语法"""

        # 移除 {collapsible="true"} 语法
        content = re.sub(r'\s*\{collapsible="true"\}', '', content)
        content = re.sub(r'\s*\{collapsible\}', '', content)

        # 移除 {style="note"} 等样式标记
        content = re.sub(r'\s*\{style="[^"]*"\}', '', content)

        # 处理 <shortcut> 标签
        content = re.sub(r'<shortcut>([^<]+)</shortcut>', r'`\1`', content)

        # 处理 Writerside 的提示块语法
        content = re.sub(r'>\s*\*\*注意\*\*\n>\s*\n>', '> **注意**\n>', content)
        content = re.sub(r'>\s*\*\*警告\*\*\n>\s*\n>', '> **警告**\n>', content)
        content = re.sub(r'>\s*\*\*提示\*\*\n>\s*\n>', '> **提示**\n>', content)

        return content

    def fix_code_blocks(self, content):
        """修复代码块的语言标识"""

        # 修复常见的语言标识
        language_fixes = {
            'Javascript': 'javascript',
            'Bash': 'bash',
            'Kotlin': 'kotlin',
            'Dart': 'dart',
            'YAML': 'yaml',
            'Json': 'json',
            'XML': 'xml'
        }

        for wrong, correct in language_fixes.items():
            content = re.sub(f'```{wrong}', f'```{correct}', content)

        return content

    def fix_image_links(self, content):
        """修复图片链接"""

        def replace_markdown_image(match):
            alt_text = match.group(1)
            image_path = match.group(2)

            # 提取文件名
            image_name = os.path.basename(image_path)

            # 确定资源类型
            resource_type = "images"
            if image_name.lower().endswith('.gif'):
                resource_type = "gif"
            elif image_name.lower().endswith(('.mp4', '.webm', '.avi')):
                resource_type = "videos"

            # 查找实际路径
            actual_path = self.find_actual_resource_path(image_name, resource_type)

            return f'![{alt_text}]({actual_path})'

        def replace_img_tag(match):
            image_path = match.group(1)
            other_attrs = match.group(2)

            # 提取文件名
            image_name = os.path.basename(image_path)

            # 确定资源类型
            resource_type = "images"
            if image_name.lower().endswith('.gif'):
                resource_type = "gif"
            elif image_name.lower().endswith(('.mp4', '.webm', '.avi')):
                resource_type = "videos"

            # 查找实际路径
            actual_path = self.find_actual_resource_path(image_name, resource_type)

            return f'<img src="{actual_path}"{other_attrs}>'

        # 应用替换
        content = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', replace_markdown_image, content)
        content = re.sub(r'<img\s+src="([^"]+)"([^>]*>)', replace_img_tag, content)

        return content

    def fix_video_syntax(self, content):
        """修复视频语法"""

        # 处理 Writerside 的视频语法
        def replace_video(match):
            video_path = match.group(1)
            video_name = os.path.basename(video_path)
            actual_path = self.find_actual_resource_path(video_name, "videos")

            return f'''<video controls>
  <source src="{actual_path}" type="video/mp4">
  您的浏览器不支持视频标签。
</video>'''

        content = re.sub(r'<video[^>]*src="([^"]+)"[^>]*></video>', replace_video, content)

        return content

    def fix_table_syntax(self, content):
        """修复表格语法"""

        # 确保表格前后有空行
        content = re.sub(r'([^\n])\n(\|)', r'\1\n\n\2', content)
        content = re.sub(r'(\|[^\n]+)\n([^\n|])', r'\1\n\n\2', content)

        return content

    def clean_empty_lines(self, content):
        """清理多余的空行"""

        # 移除连续的多个空行，保留最多两个连续空行
        content = re.sub(r'\n{4,}', '\n\n\n', content)

        # 移除行尾空格
        content = re.sub(r' +\n', '\n', content)

        return content

    def process_file(self, file_path):
        """处理单个文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            original_content = content

            # 应用所有修复
            content = self.fix_writerside_syntax(content)
            content = self.fix_code_blocks(content)
            content = self.fix_image_links(content)
            content = self.fix_video_syntax(content)
            content = self.fix_table_syntax(content)
            content = self.clean_empty_lines(content)

            if original_content != content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"修复了文档: {file_path}")
                return True

        except Exception as e:
            print(f"处理文件 {file_path} 时出错: {e}")

        return False

    def convert_topic_files(self):
        """转换 .topic 文件到 markdown"""
        print("转换 .topic 文件...")

        topics_dir = self.writerside_path / "topics"
        if not topics_dir.exists():
            return

        for topic_file in topics_dir.rglob("*.topic"):
            try:
                # 解析 XML
                tree = ET.parse(topic_file)
                root = tree.getroot()

                # 提取标题
                title = root.get('title', topic_file.stem)

                # 转换内容
                content = f"# {title}\n\n"
                content += self._convert_xml_to_markdown(root)

                # 确定目标路径
                relative_path = topic_file.relative_to(topics_dir)
                target_path = self.docs_path / relative_path.with_suffix('.md')

                # 创建目录
                target_path.parent.mkdir(parents=True, exist_ok=True)

                # 写入文件
                with open(target_path, 'w', encoding='utf-8') as f:
                    f.write(content)

                print(f"转换了 topic 文件: {topic_file} -> {target_path}")

            except Exception as e:
                print(f"转换 topic 文件 {topic_file} 时出错: {e}")

    def _convert_xml_to_markdown(self, element):
        """将 XML 元素转换为 Markdown"""
        content = ""

        if element.text:
            content += element.text.strip()

        for child in element:
            if child.tag == 'p':
                content += "\n\n" + (child.text or "").strip()
            elif child.tag == 'chapter':
                title = child.get('title', '')
                if title:
                    content += f"\n\n## {title}\n\n"
                content += self._convert_xml_to_markdown(child)
            elif child.tag == 'code-block':
                lang = child.get('lang', '')
                code_content = child.text or ""
                content += f"\n\n```{lang}\n{code_content.strip()}\n```\n\n"
            elif child.tag == 'img':
                src = child.get('src', '')
                alt = child.get('alt', '')
                content += f"\n\n![{alt}]({src})\n\n"
            elif child.tag == 'list':
                content += "\n\n"
                for item in child.findall('li'):
                    content += f"- {item.text or ''}\n"
                content += "\n"
            else:
                content += self._convert_xml_to_markdown(child)

            if child.tail:
                content += child.tail.strip()

        return content

    def run(self):
        """运行修复程序"""
        print("开始增强修复文档...")

        # 1. 复制缺失的资源文件
        self.copy_missing_resources()

        # 2. 转换 .topic 文件
        self.convert_topic_files()

        # 3. 修复所有 markdown 文件
        fixed_count = 0
        for md_file in self.docs_path.rglob("*.md"):
            if self.process_file(md_file):
                fixed_count += 1

        print(f"完成！共修复了 {fixed_count} 个文件。")

if __name__ == "__main__":
    fixer = EnhancedDocFixer()
    fixer.run()
