#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
from pathlib import Path
import shutil

class FinalImageLinksFixer:
    def __init__(self):
        self.docs_path = Path("flutterx-doc/docs")
        self.public_path = Path("flutterx-doc/docs/public")
        self.writerside_path = Path("Writerside")

    def ensure_all_resources_copied(self):
        """确保所有资源都已复制"""
        print("确保所有资源文件已复制...")

        # 复制所有图片资源
        if (self.writerside_path / "images").exists():
            for img_file in (self.writerside_path / "images").rglob("*"):
                if img_file.is_file():
                    relative_path = img_file.relative_to(self.writerside_path / "images")
                    target_file = self.public_path / "images" / relative_path

                    if not target_file.exists():
                        target_file.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(img_file, target_file)
                        print(f"复制图片: {img_file} -> {target_file}")

        # 复制所有GIF资源
        if (self.writerside_path / "gif").exists():
            for gif_file in (self.writerside_path / "gif").rglob("*"):
                if gif_file.is_file():
                    relative_path = gif_file.relative_to(self.writerside_path / "gif")
                    target_file = self.public_path / "gif" / relative_path

                    if not target_file.exists():
                        target_file.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(gif_file, target_file)
                        print(f"复制GIF: {gif_file} -> {target_file}")

        # 复制所有视频资源
        if (self.writerside_path / "videos").exists():
            for video_file in (self.writerside_path / "videos").rglob("*"):
                if video_file.is_file():
                    relative_path = video_file.relative_to(self.writerside_path / "videos")
                    target_file = self.public_path / "videos" / relative_path

                    if not target_file.exists():
                        target_file.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(video_file, target_file)
                        print(f"复制视频: {video_file} -> {target_file}")

    def create_missing_images(self):
        """为缺失的图片创建占位符"""
        print("为缺失的图片创建占位符...")

        missing_images = [
            "ds.JPG",
            "dd_check_plugin",
            "scan_ios.png",
            "ios-17-scan-dialog.png"
        ]

        for img_name in missing_images:
            img_path = self.public_path / "images" / img_name
            if not img_path.exists():
                # 创建一个简单的占位符文件
                img_path.parent.mkdir(parents=True, exist_ok=True)
                with open(img_path, 'w', encoding='utf-8') as f:
                    f.write(f"# 占位符: {img_name}\n这是一个占位符文件，请替换为实际图片。")
                print(f"创建占位符: {img_path}")

    def find_actual_image_path(self, image_name):
        """查找实际的图片路径"""
        # 移除文件名中的下划线前缀
        clean_name = image_name.lstrip('_')

        # 搜索所有可能的位置
        search_paths = [
            self.public_path / "images",
            self.public_path / "gif",
            self.public_path / "videos"
        ]

        for search_path in search_paths:
            if not search_path.exists():
                continue

            # 精确匹配
            for root, dirs, files in os.walk(search_path):
                for file in files:
                    if file == image_name or file == clean_name:
                        relative_path = os.path.relpath(os.path.join(root, file), self.public_path)
                        return f"/{relative_path}"

            # 模糊匹配
            for root, dirs, files in os.walk(search_path):
                for file in files:
                    if clean_name in file or file in clean_name:
                        relative_path = os.path.relpath(os.path.join(root, file), self.public_path)
                        return f"/{relative_path}"

        # 默认路径
        if image_name.lower().endswith('.gif'):
            return f"/gif/{image_name}"
        elif image_name.lower().endswith(('.mp4', '.webm', '.avi')):
            return f"/videos/{image_name}"
        else:
            return f"/images/{image_name}"

    def fix_image_links_in_file(self, file_path):
        """修复单个文件中的图片链接"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            original_content = content

            # 修复 Markdown 图片链接 ![alt](path)
            def replace_markdown_image(match):
                alt_text = match.group(1)
                image_path = match.group(2)

                # 如果已经是正确的绝对路径，不修改
                if image_path.startswith('/') and (
                    self.public_path / image_path.lstrip('/')
                ).exists():
                    return match.group(0)

                # 提取文件名
                image_name = os.path.basename(image_path)
                actual_path = self.find_actual_image_path(image_name)

                return f'![{alt_text}]({actual_path})'

            # 修复 HTML img 标签
            def replace_img_tag(match):
                full_match = match.group(0)
                image_path = match.group(1)

                # 如果已经是正确的绝对路径，不修改
                if image_path.startswith('/') and (
                    self.public_path / image_path.lstrip('/')
                ).exists():
                    return full_match

                # 提取文件名
                image_name = os.path.basename(image_path)
                actual_path = self.find_actual_image_path(image_name)

                return full_match.replace(f'src="{image_path}"', f'src="{actual_path}"')

            # 应用替换
            content = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', replace_markdown_image, content)
            content = re.sub(r'(<img[^>]+src=")([^"]+)("[^>]*>)', replace_img_tag, content)

            # 修复一些特殊的图片链接格式
            content = re.sub(r'\[!\[([^\]]*)\]\(([^)]+)\)\]\(([^)]+)\)',
                           lambda m: f'[![{m.group(1)}]({self.find_actual_image_path(os.path.basename(m.group(2)))})]({m.group(3)})',
                           content)

            if original_content != content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"修复图片链接: {file_path.relative_to(self.docs_path)}")
                return True

        except Exception as e:
            print(f"处理文件 {file_path} 时出错: {e}")

        return False

    def create_image_index(self):
        """创建图片索引文件，方便检查"""
        print("创建图片索引...")

        index_content = "# 图片资源索引\n\n这是自动生成的图片资源索引文件。\n\n"

        if self.public_path.exists():
            for img_file in self.public_path.rglob("*"):
                if img_file.is_file() and img_file.suffix.lower() in ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp']:
                    relative_path = img_file.relative_to(self.public_path)
                    index_content += f"- `/{relative_path.as_posix()}`\n"

        with open(self.docs_path / "image_index.md", 'w', encoding='utf-8') as f:
            f.write(index_content)

    def run(self):
        """运行最终的图片链接修复"""
        print("开始最终图片链接修复...")
        print("=" * 50)

        # 1. 确保所有资源都已复制
        self.ensure_all_resources_copied()

        # 2. 创建缺失图片的占位符
        self.create_missing_images()

        # 3. 修复所有文档中的图片链接
        fixed_count = 0
        for md_file in self.docs_path.rglob("*.md"):
            if md_file.name == "image_index.md":
                continue
            if self.fix_image_links_in_file(md_file):
                fixed_count += 1

        # 4. 创建图片索引
        self.create_image_index()

        print("=" * 50)
        print(f"图片链接修复完成！共修复了 {fixed_count} 个文件。")
        print("\n修复内容:")
        print("✅ 复制了所有缺失的资源文件")
        print("✅ 为缺失的图片创建了占位符")
        print("✅ 修复了所有文档中的图片链接")
        print("✅ 创建了图片资源索引")

        print("\n下一步:")
        print("1. 检查 docs/image_index.md 确认所有图片都已正确索引")
        print("2. 替换占位符文件为实际图片")
        print("3. 运行 rspress 开发服务器测试: cd flutterx-doc && npm run dev")

if __name__ == "__main__":
    fixer = FinalImageLinksFixer()
    fixer.run()
