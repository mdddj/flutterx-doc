#!/bin/bash

# FlutterX 文档部署脚本

echo "开始构建文档..."
npm run build

if [ $? -eq 0 ]; then
    echo "文档构建成功!"
    
    # 检查是否已安装 gh CLI 工具
    if command -v gh &> /dev/null; then
        echo "触发 GitHub Actions 工作流..."
        gh workflow run deploy-pages.yml -R mdddj/flutterx-doc
        
        if [ $? -eq 0 ]; then
            echo "GitHub Actions 工作流已成功触发!"
            echo "您可以通过以下链接查看部署状态:"
            echo "https://github.com/mdddj/flutterx-doc/actions"
        else
            echo "触发 GitHub Actions 工作流失败!"
        fi
    else
        echo "未安装 GitHub CLI (gh)。请手动访问以下链接触发部署:"
        echo "https://github.com/mdddj/flutterx-doc/actions/workflows/deploy-pages.yml"
    fi
else
    echo "文档构建失败! 请检查错误信息。"
    exit 1
fi
