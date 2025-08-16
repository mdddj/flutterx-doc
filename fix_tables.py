#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
from pathlib import Path

class TableFixer:
    def __init__(self):
        self.docs_path = Path("flutterx-doc/docs")

    def fix_table_formatting(self, content):
        """修复表格格式"""
        lines = content.split('\n')
        fixed_lines = []
        i = 0

        while i < len(lines):
            line = lines[i]

            # 检测表格开始（包含|的行）
            if '|' in line and line.strip():
                # 确保表格前有空行
                if fixed_lines and fixed_lines[-1].strip():
                    fixed_lines.append('')

                # 处理表格
                table_lines = []
                j = i

                # 收集所有表格行
                while j < len(lines) and '|' in lines[j] and lines[j].strip():
                    table_lines.append(lines[j].strip())
                    j += 1

                if len(table_lines) >= 1:
                    # 添加第一行（表头）
                    header = table_lines[0]
                    fixed_lines.append(header)

                    # 检查是否已有分隔行
                    has_separator = len(table_lines) > 1 and '---' in table_lines[1]

                    if not has_separator:
                        # 创建分隔行
                        col_count = header.count('|') - 1
                        if header.startswith('|') and header.endswith('|'):
                            separator = '|' + '---|' * col_count
                        else:
                            separator = '|' + '---|' * (col_count + 1)
                        fixed_lines.append(separator)

                        # 添加数据行
                        for table_line in table_lines[1:]:
                            fixed_lines.append(table_line)
                    else:
                        # 已有分隔行，直接添加剩余行
                        for table_line in table_lines[1:]:
                            fixed_lines.append(table_line)

                # 确保表格后有空行
                if j < len(lines) and lines[j].strip():
                    fixed_lines.append('')

                i = j
            else:
                fixed_lines.append(line)
                i += 1

        return '\n'.join(fixed_lines)

    def process_file(self, file_path):
        """处理单个文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            original_content = content
            fixed_content = self.fix_table_formatting(content)

            if original_content != fixed_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(fixed_content)
                print(f"修复了表格格式: {file_path}")
                return True

        except Exception as e:
            print(f"处理文件 {file_path} 时出错: {e}")

        return False

    def run(self):
        """运行修复程序"""
        print("开始修复表格格式...")

        fixed_count = 0

        # 遍历所有 markdown 文件
        for md_file in self.docs_path.rglob("*.md"):
            if self.process_file(md_file):
                fixed_count += 1

        print(f"完成！共修复了 {fixed_count} 个文件的表格格式。")

if __name__ == "__main__":
    fixer = TableFixer()
    fixer.run()
