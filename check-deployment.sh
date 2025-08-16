#!/bin/bash

# 检查 GitHub Pages 部署状态的脚本

echo "检查仓库信息..."
curl -s -H "Accept: application/vnd.github.v3+json" https://api.github.com/repos/mdddj/flutterx-doc | grep -E "full_name|html_url|homepage|has_pages"

echo ""
echo "检查最近的工作流运行..."
curl -s -H "Accept: application/vnd.github.v3+json" https://api.github.com/repos/mdddj/flutterx-doc/actions/runs | jq -r '.workflow_runs[0] | "工作流ID: \(.id)\n状态: \(.status)\n结论: \(.conclusion)\n分支: \(.head_branch)\n创建时间: \(.created_at)"'

echo ""
echo "检查 GitHub Pages 设置..."
curl -s -H "Accept: application/vnd.github.v3+json" https://api.github.com/repos/mdddj/flutterx-doc/pages
