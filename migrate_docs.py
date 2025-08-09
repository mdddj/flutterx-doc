#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
import re
import xml.etree.ElementTree as ET
from pathlib import Path
import json

class DocMigrator:
    def __init__(self):
        self.writerside_path = Path("Writerside")
        self.rspress_path = Path("flutterx-doc/docs")
        self.topics_path = self.writerside_path / "topics"
        self.images_path = self.writerside_path / "images"
        self.gif_path = self.writerside_path / "gif"
        self.videos_path = self.writerside_path / "videos"

        # 目录映射
        self.dir_mapping = {
            "dio": ["Starter.md", "接口信息截图.md"],
            "shared_p": ["Shared_preferences.md"],
            "hive": ["Hive缓存工具.md"],
            "riverpod": ["Riverpod-Widget-Tool.md"],
            "freezed": [
                "freezed-3-x版本迁移工具.topic",
                "Json-to-Freezed.topic",
                "generate.topic",
                "Freezed-Class-Tool-Menu.md"
            ],
            "dart-file": [
                "资产文件路径检查功能.topic",
                "资产字符串快速打开文件.md",
                "资产图片预览功能.md",
                "Project-Library-scan.topic",
                "参数类型内联显示.md"
            ],
            "pubspec": [
                "不再更新的三方包检测.topic",
                "第三方包工具.md"
            ],
            "other": [
                "Log.topic",
                "l10n-editor.topic",
                "flutter3-29-0安卓迁移gradle工具.topic",
                "ios-17-隐私扫描工具.md",
                "flutter新版本检测.md"
            ],
            "assets": [
                "资产预览窗口.md",
                "资产预览.md",
                "资产生成类调用.md"
            ],
            "settings": [
                "riverpod.md",
                "快速打开子目录文件夹.md",
                "Links.md",
                "内联资产显示.md"
            ]
        }

    def convert_image_links(self, content):
        """转换图片链接路径"""
        # 处理 ![alt](image.png) 格式
        content = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', self._replace_image_link, content)

        # 处理 <img src="path" alt="alt"> 格式
        content = re.sub(r'<img\s+src="([^"]+)"([^>]*)>', self._replace_img_tag, content)

        return content

    def _replace_image_link(self, match):
        alt_text = match.group(1)
        image_path = match.group(2)

        # 转换路径
        new_path = self._convert_path(image_path)
        return f'![{alt_text}]({new_path})'

    def _replace_img_tag(self, match):
        image_path = match.group(1)
        other_attrs = match.group(2)

        # 转换路径
        new_path = self._convert_path(image_path)
        return f'<img src="{new_path}"{other_attrs}>'

    def _convert_path(self, path):
        """转换图片路径"""
        # 移除开头的 ../images/ 或类似路径
        path = path.replace('../images/', '')
        path = path.replace('images/', '')
        path = path.replace('../gif/', '')
        path = path.replace('gif/', '')
        path = path.replace('../videos/', '')
        path = path.replace('videos/', '')

        # 如果路径以 _ 开头，说明是相对路径的图片
        if path.startswith('_'):
            path = path[1:]  # 移除开头的下划线

        # 检查文件扩展名，确定资源类型
        if path.endswith('.gif'):
            if path.startswith('gif/'):
                return f'/gif/{path[4:]}'
            else:
                return f'/gif/{path}'
        elif path.endswith(('.mp4', '.avi', '.mov')):
            if path.startswith('videos/'):
                return f'/videos/{path[7:]}'
            else:
                return f'/videos/{path}'
        else:
            # 图片文件
            if path.startswith('images/'):
                return f'/images/{path[7:]}'
            else:
                return f'/images/{path}'

    def convert_topic_to_md(self, topic_file):
        """将 .topic XML 文件转换为 Markdown"""
        try:
            tree = ET.parse(topic_file)
            root = tree.getroot()

            # 获取标题
            title = root.get('title', os.path.splitext(os.path.basename(topic_file))[0])

            md_content = f"# {title}\n\n"

            # 递归处理 XML 元素
            md_content += self._process_xml_element(root)

            return md_content
        except Exception as e:
            print(f"转换 {topic_file} 失败: {e}")
            return f"# {os.path.splitext(os.path.basename(topic_file))[0]}\n\n转换失败，请手动处理。\n"

    def _process_xml_element(self, element, level=0):
        """递归处理XML元素转换为Markdown"""
        content = ""

        # 处理不同的XML标签
        if element.tag == 'p':
            text = element.text or ""
            for child in element:
                text += self._process_xml_element(child, level)
                if child.tail:
                    text += child.tail
            content += f"{text}\n\n"

        elif element.tag == 'chapter':
            title = element.get('title', '')
            if title:
                content += f"{'#' * (level + 2)} {title}\n\n"
            for child in element:
                content += self._process_xml_element(child, level + 1)

        elif element.tag == 'procedure':
            title = element.get('title', '')
            if title:
                content += f"{'#' * (level + 2)} {title}\n\n"
            for child in element:
                content += self._process_xml_element(child, level)

        elif element.tag == 'step':
            text = element.text or ""
            for child in element:
                text += self._process_xml_element(child, level)
                if child.tail:
                    text += child.tail
            content += f"1. {text}\n"

        elif element.tag == 'code':
            text = element.text or ""
            content += f"`{text}`"

        elif element.tag == 'code-block':
            lang = element.get('lang', '')
            text = element.text or ""
            content += f"```{lang}\n{text}\n```\n\n"

        elif element.tag == 'img':
            src = element.get('src', '')
            alt = element.get('alt', '')
            new_src = self._convert_path(src)
            content += f"![{alt}]({new_src})\n\n"

        elif element.tag == 'a':
            href = element.get('href', '')
            text = element.text or ""
            content += f"[{text}]({href})"

        elif element.tag == 'note':
            text = ""
            for child in element:
                text += self._process_xml_element(child, level)
            content += f"> **注意**\n> \n> {text}\n\n"

        elif element.tag == 'warning':
            text = ""
            for child in element:
                text += self._process_xml_element(child, level)
            content += f"> **警告**\n> \n> {text}\n\n"

        elif element.tag == 'control':
            text = element.text or ""
            content += f"**{text}**"

        elif element.tag == 'shortcut':
            text = element.text or ""
            content += f"`{text}`"

        else:
            # 默认处理：提取文本内容
            if element.text:
                content += element.text
            for child in element:
                content += self._process_xml_element(child, level)
                if child.tail:
                    content += child.tail

        return content

    def migrate_file(self, source_file, target_dir):
        """迁移单个文件"""
        source_path = self.topics_path / source_file

        if not source_path.exists():
            # 检查是否在子目录中
            for subdir in self.topics_path.iterdir():
                if subdir.is_dir():
                    sub_file = subdir / source_file
                    if sub_file.exists():
                        source_path = sub_file
                        break

        if not source_path.exists():
            print(f"文件不存在: {source_file}")
            return

        target_path = self.rspress_path / target_dir
        target_path.mkdir(parents=True, exist_ok=True)

        if source_file.endswith('.topic'):
            # 转换 .topic 文件为 .md
            md_content = self.convert_topic_to_md(source_path)
            md_content = self.convert_image_links(md_content)

            target_file = target_path / (source_file.replace('.topic', '.md'))
            with open(target_file, 'w', encoding='utf-8') as f:
                f.write(md_content)
            print(f"转换并迁移: {source_file} -> {target_file}")

        elif source_file.endswith('.md'):
            # 直接复制 .md 文件并转换图片链接
            with open(source_path, 'r', encoding='utf-8') as f:
                content = f.read()

            content = self.convert_image_links(content)

            target_file = target_path / source_file
            with open(target_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"迁移: {source_file} -> {target_file}")

    def migrate_root_files(self):
        """迁移根目录的文件"""
        root_files = ["打赏.md", "更新日志.topic", "安装.topic"]

        for file_name in root_files:
            source_path = self.topics_path / file_name
            if source_path.exists():
                if file_name.endswith('.topic'):
                    # 转换为 .md
                    md_content = self.convert_topic_to_md(source_path)
                    md_content = self.convert_image_links(md_content)

                    target_file = self.rspress_path / file_name.replace('.topic', '.md')
                    with open(target_file, 'w', encoding='utf-8') as f:
                        f.write(md_content)
                    print(f"转换根文件: {file_name} -> {target_file}")

                else:
                    # 直接复制
                    with open(source_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    content = self.convert_image_links(content)

                    target_file = self.rspress_path / file_name
                    with open(target_file, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"迁移根文件: {file_name} -> {target_file}")

    def update_rspress_config(self):
        """更新 rspress 配置文件"""
        config_path = Path("flutterx-doc/rspress.config.ts")

        config_content = '''import * as path from 'node:path';
import { defineConfig } from 'rspress/config';

export default defineConfig({
  root: path.join(__dirname, 'docs'),
  title: 'FlutterX 插件文档',
  description: 'FlutterX - Flutter开发者快速开发的辅助工具插件',
  icon: '/logo.svg',
  logo: {
    light: '/logo.svg',
    dark: '/logo.svg',
  },
  themeConfig: {
    socialLinks: [
      {
        icon: 'github',
        mode: 'link',
        content: 'https://github.com/mdddj/dd_flutter_idea_plugin',
      },
    ],
    nav: [
      {
        text: '首页',
        link: '/',
      },
      {
        text: '文档',
        link: '/安装',
      },
    ],
    sidebar: {
      '/': [
        {
          text: '开始使用',
          items: [
            {
              text: '安装',
              link: '/安装',
            },
          ],
        },
        {
          text: 'Dio',
          items: [
            {
              text: 'Dio接口监听',
              link: '/dio/Starter',
            },
            {
              text: '接口信息截图',
              link: '/dio/接口信息截图',
            },
          ],
        },
        {
          text: 'Shared Preferences',
          items: [
            {
              text: 'Shared Preferences',
              link: '/shared_p/Shared_preferences',
            },
          ],
        },
        {
          text: 'Hive',
          items: [
            {
              text: 'Hive缓存工具',
              link: '/hive/Hive缓存工具',
            },
          ],
        },
        {
          text: 'Riverpod',
          items: [
            {
              text: 'Riverpod Widget Tool',
              link: '/riverpod/Riverpod-Widget-Tool',
            },
          ],
        },
        {
          text: 'Freezed',
          items: [
            {
              text: 'Freezed 3.x版本迁移工具',
              link: '/freezed/freezed-3-x版本迁移工具',
            },
            {
              text: 'Json to Freezed',
              link: '/freezed/Json-to-Freezed',
            },
            {
              text: '代码生成',
              link: '/freezed/generate',
            },
            {
              text: 'Freezed Class Tool Menu',
              link: '/freezed/Freezed-Class-Tool-Menu',
            },
          ],
        },
        {
          text: 'Dart File',
          items: [
            {
              text: '资产文件路径检查功能',
              link: '/dart-file/资产文件路径检查功能',
            },
            {
              text: '资产字符串快速打开文件',
              link: '/dart-file/资产字符串快速打开文件',
            },
            {
              text: '资产图片预览功能',
              link: '/dart-file/资产图片预览功能',
            },
            {
              text: 'Project Library Scan',
              link: '/dart-file/Project-Library-scan',
            },
            {
              text: '参数类型内联显示',
              link: '/dart-file/参数类型内联显示',
            },
          ],
        },
        {
          text: 'Pubspec.yaml',
          items: [
            {
              text: '不再更新的三方包检测',
              link: '/pubspec/不再更新的三方包检测',
            },
            {
              text: '第三方包工具',
              link: '/pubspec/第三方包工具',
            },
          ],
        },
        {
          text: '其他功能',
          items: [
            {
              text: '日志工具',
              link: '/other/Log',
            },
            {
              text: 'L10n编辑器',
              link: '/other/l10n-editor',
            },
            {
              text: 'Flutter 3.29.0 安卓迁移 Gradle 工具',
              link: '/other/flutter3-29-0安卓迁移gradle工具',
            },
            {
              text: 'iOS 17 隐私扫描工具',
              link: '/other/ios-17-隐私扫描工具',
            },
            {
              text: 'Flutter新版本检测',
              link: '/other/flutter新版本检测',
            },
          ],
        },
        {
          text: '资产管理',
          items: [
            {
              text: '资产预览窗口',
              link: '/assets/资产预览窗口',
            },
            {
              text: '资产预览',
              link: '/assets/资产预览',
            },
            {
              text: '资产生成类调用',
              link: '/assets/资产生成类调用',
            },
          ],
        },
        {
          text: '设置',
          items: [
            {
              text: 'Riverpod设置',
              link: '/settings/riverpod',
            },
            {
              text: '快速打开子目录文件夹',
              link: '/settings/快速打开子目录文件夹',
            },
            {
              text: '链接',
              link: '/settings/Links',
            },
            {
              text: '内联资产显示',
              link: '/settings/内联资产显示',
            },
          ],
        },
        {
          text: '其他',
          items: [
            {
              text: '打赏',
              link: '/打赏',
            },
            {
              text: '更新日志',
              link: '/更新日志',
            },
          ],
        },
      ],
    },
  },
});
'''

        with open(config_path, 'w', encoding='utf-8') as f:
            f.write(config_content)
        print(f"更新配置文件: {config_path}")

    def create_index_page(self):
        """创建首页"""
        index_content = """# FlutterX 插件文档

欢迎使用 FlutterX 插件！这是一个为 Flutter 开发者提供的强大辅助工具插件。

## 主要功能

- **Dio 请求监听** - 实时监控和查看网络请求
- **JSON 转 Freezed** - 快速将 JSON 转换为 Freezed 模型
- **Hive 可视化** - 可视化查看 Hive 缓存数据
- **Shared Preferences 管理** - 可视化管理应用偏好设置
- **资产管理工具** - 强大的资产文件管理和预览功能
- **代码生成工具** - 自动生成常用代码模板

## 快速开始

1. [安装插件](./安装.md)
2. 选择你需要的功能开始使用

## 开源信息

FlutterX 是一个开源且免费的项目，由梁典典开发维护。

- **GitHub**: [https://github.com/mdddj/dd_flutter_idea_plugin](https://github.com/mdddj/dd_flutter_idea_plugin)
- **官网**: [https://flutterx.itbug.shop](https://flutterx.itbug.shop)

## 支持作者

如果这个插件对你有帮助，欢迎[打赏支持](./打赏.md)！
"""

        index_path = self.rspress_path / "index.md"
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(index_content)
        print(f"创建首页: {index_path}")

    def run(self):
        """执行迁移"""
        print("开始迁移文档...")

        # 迁移分类文档
        for category, files in self.dir_mapping.items():
            print(f"迁移 {category} 类别文档...")
            for file_name in files:
                self.migrate_file(file_name, category)

        # 迁移根目录文件
        print("迁移根目录文件...")
        self.migrate_root_files()

        # 创建首页
        print("创建首页...")
        self.create_index_page()

        # 更新配置文件
        print("更新配置文件...")
        self.update_rspress_config()

        print("文档迁移完成！")

if __name__ == "__main__":
    migrator = DocMigrator()
    migrator.run()
