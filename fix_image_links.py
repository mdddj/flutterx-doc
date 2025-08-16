#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
from pathlib import Path

class ImageLinkFixer:
    def __init__(self):
        self.docs_path = Path("flutterx-doc/docs")
        self.images_path = Path("flutterx-doc/docs/public/images")

    def find_actual_image_path(self, image_name):
        """在图片目录中查找实际的图片路径"""
        # 移除开头的下划线（如果有）
        clean_name = image_name.lstrip('_')

        # 在所有子目录中搜索图片
        for root, dirs, files in os.walk(self.images_path):
            for file in files:
                if file == image_name or file == clean_name:
                    # 返回相对于 public 目录的路径
                    relative_path = os.path.relpath(os.path.join(root, file), self.images_path.parent)
                    return f"/{relative_path}"

        # 如果找不到，尝试搜索类似的文件名
        for root, dirs, files in os.walk(self.images_path):
            for file in files:
                if clean_name in file or file in clean_name:
                    relative_path = os.path.relpath(os.path.join(root, file), self.images_path.parent)
                    return f"/{relative_path}"

        # 如果仍然找不到，返回默认路径
        return f"/images/{image_name}"

    def fix_image_links(self, content):
        """修复文档中的图片链接"""

        # 处理 ![alt](image.png) 格式
        def replace_markdown_image(match):
            alt_text = match.group(1)
            image_path = match.group(2)

            # 提取文件名
            image_name = os.path.basename(image_path)

            # 查找实际路径
            actual_path = self.find_actual_image_path(image_name)

            return f'![{alt_text}]({actual_path})'

        # 处理 <img src="path" alt="alt"> 格式
        def replace_img_tag(match):
            image_path = match.group(1)
            other_attrs = match.group(2)

            # 提取文件名
            image_name = os.path.basename(image_path)

            # 查找实际路径
            actual_path = self.find_actual_image_path(image_name)

            return f'<img src="{actual_path}"{other_attrs}>'

        # 应用替换
        content = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', replace_markdown_image, content)
        content = re.sub(r'<img\s+src="([^"]+)"([^>]*>)', replace_img_tag, content)

        return content

    def process_file(self, file_path):
        """处理单个文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            original_content = content
            fixed_content = self.fix_image_links(content)

            if original_content != fixed_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(fixed_content)
                print(f"修复了图片链接: {file_path}")
                return True

        except Exception as e:
            print(f"处理文件 {file_path} 时出错: {e}")

        return False

    def run(self):
        """运行修复程序"""
        print("开始修复图片链接...")

        fixed_count = 0

        # 遍历所有 markdown 文件
        for md_file in self.docs_path.rglob("*.md"):
            if self.process_file(md_file):
                fixed_count += 1

        print(f"完成！共修复了 {fixed_count} 个文件的图片链接。")

if __name__ == "__main__":
    fixer = ImageLinkFixer()
    fixer.run()
