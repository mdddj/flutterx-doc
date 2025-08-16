#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
from pathlib import Path

class AdvancedTableFixer:
    def __init__(self):
        self.docs_path = Path("flutterx-doc/docs")

    def fix_table_formatting(self, content):
        """修复表格格式"""
        # 使用正则表达式查找并修复表格
        def fix_table_match(match):
            table_content = match.group(0)
            lines = table_content.strip().split('\n')

            # 过滤掉空行和无效行
            valid_lines = []
            for line in lines:
                line = line.strip()
                if line and '|' in line:
                    valid_lines.append(line)

            if len(valid_lines) < 1:
                return table_content

            # 确保所有行都以|开头和结尾
            normalized_lines = []
            for line in valid_lines:
                if not line.startswith('|'):
                    line = '|' + line
                if not line.endswith('|'):
                    line = line + '|'
                normalized_lines.append(line)

            # 检查是否有分隔行
            has_separator = False
            separator_index = -1

            for i, line in enumerate(normalized_lines):
                if '---' in line or '-|-' in line:
                    has_separator = True
                    separator_index = i
                    break

            result_lines = []

            if len(normalized_lines) >= 1:
                # 添加表头
                header = normalized_lines[0]
                result_lines.append(header)

                if not has_separator:
                    # 创建分隔行
                    parts = header.split('|')
                    separator_parts = []
                    for part in parts:
                        if part.strip():
                            separator_parts.append('---')
                        else:
                            separator_parts.append('')
                    separator = '|'.join(separator_parts)
                    result_lines.append(separator)

                    # 添加数据行
                    for line in normalized_lines[1:]:
                        result_lines.append(line)
                else:
                    # 已有分隔行，保持原有结构
                    for line in normalized_lines[1:]:
                        result_lines.append(line)

            return '\n\n' + '\n'.join(result_lines) + '\n\n'

        # 查找表格模式（连续的包含|的行）
        table_pattern = r'(?:\n|^)(?:\|[^\n]*\|?\n?)+'
        content = re.sub(table_pattern, fix_table_match, content, flags=re.MULTILINE)

        return content

    def manual_fix_dio_table(self):
        """手动修复 Dio 文档中的表格"""
        dio_file = self.docs_path / "dio" / "Starter.md"

        if not dio_file.exists():
            return

        with open(dio_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # 手动替换表格部分
        table_content = '''
| 参数 | 说明 |
|---|---|
| initHost | 你的本机 IP, 不要设置成 127.0.0.1,不然真机模式下连不上,键入`1`插件会有自动补全,选择就行 |
| port | 监听端口,默认 9999,可以在设置里面更改,没啥特殊需求就不要改了,修改这个设置后记得重启 AS |
| projectName | 自定义你的项目名字 |
| customCoverterResponseData | 这里可以修改传到 idea 里面的数据模型,没啥事也不用改. 但是可以添加额外的备注信息 |
| timeOut | 连接 idea 插件的超时时间 |
| hostHandle | 如果不传 initHost,函数会扫描你的 IP 段,尝试自动连接,一般用不上 |
| version | 传输数据格式版本,这里一般不用改 |
| conectSuccess | 连接插件成功的回调,回调一个连接 scoket对象,一般用不上 |
| extend | 其他的一些工具扩展,比如 Hive工具的扩展: `HiveToolManager` ,你也可以实现`ServerMessageHandle`接口来处理idea 插件发送过来的数据 |
'''

        # 查找表格位置并替换
        pattern = r'下面是`DdCheckPlugin#init`函数的一些属性说明\n\n.*?(?=\n## |\n\n## |$)'
        replacement = f'下面是`DdCheckPlugin#init`函数的一些属性说明\n{table_content}'

        content = re.sub(pattern, replacement, content, flags=re.DOTALL)

        with open(dio_file, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"手动修复了 Dio 文档的表格: {dio_file}")

    def fix_empty_links(self, content):
        """修复空链接"""
        # 修复 freezed 链接
        content = re.sub(r'\[([^\]]*)\]\(\)', r'[\1](https://pub.dev/packages/freezed)', content)
        return content

    def process_file(self, file_path):
        """处理单个文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            original_content = content

            # 应用修复
            content = self.fix_table_formatting(content)
            content = self.fix_empty_links(content)

            if original_content != content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"修复了文档: {file_path}")
                return True

        except Exception as e:
            print(f"处理文件 {file_path} 时出错: {e}")

        return False

    def run(self):
        """运行修复程序"""
        print("开始高级表格修复...")

        # 首先手动修复 Dio 文档的表格
        self.manual_fix_dio_table()

        fixed_count = 0

        # 遍历所有 markdown 文件
        for md_file in self.docs_path.rglob("*.md"):
            if md_file.name == "Starter.md" and md_file.parent.name == "dio":
                continue  # 已经手动处理过了

            if self.process_file(md_file):
                fixed_count += 1

        print(f"完成！共修复了 {fixed_count + 1} 个文件。")

if __name__ == "__main__":
    fixer = AdvancedTableFixer()
    fixer.run()
