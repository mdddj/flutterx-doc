#!/usr/bin/env python3
"""
Build navigation structure for mkdocs based on rspress configuration
"""

import re
from pathlib import Path
from typing import Dict, List, Any

class NavigationBuilder:
    def __init__(self, mkdocs_config_path: str):
        self.mkdocs_config_path = Path(mkdocs_config_path)
        self.log_messages = []
    
    def log(self, message: str):
        """Log messages"""
        print(message)
        self.log_messages.append(message)
    
    def build_navigation_structure(self) -> Dict[str, Any]:
        """Build the complete navigation structure"""
        
        self.log("Building navigation structure...")
        
        # Define the navigation structure based on the rspress config
        navigation = {
            'zh': {
                'label': '简体中文',
                'items': [
                    {'text': '首页', 'link': 'zh/index.md'},
                    {
                        'text': '开始使用',
                        'items': [
                            {'text': '安装', 'link': 'zh/安装.md'}
                        ]
                    },
                    {
                        'text': 'Dio',
                        'items': [
                            {'text': 'Dio接口监听', 'link': 'zh/dio/Starter.md'},
                            {'text': '接口信息截图', 'link': 'zh/dio/接口信息截图.md'}
                        ]
                    },
                    {
                        'text': 'Shared Preferences',
                        'items': [
                            {'text': 'Shared Preferences', 'link': 'zh/shared_p/Shared_preferences.md'}
                        ]
                    },
                    {
                        'text': 'Hive',
                        'items': [
                            {'text': 'Hive缓存工具', 'link': 'zh/hive/Hive缓存工具.md'}
                        ]
                    },
                    {
                        'text': 'Riverpod',
                        'items': [
                            {'text': 'Riverpod Widget Tool', 'link': 'zh/riverpod/Riverpod-Widget-Tool.md'},
                            {'text': 'Riverpod设置', 'link': 'zh/settings/riverpod.md'}
                        ]
                    },
                    {
                        'text': 'Freezed',
                        'items': [
                            {'text': 'Freezed 3.x版本迁移工具', 'link': 'zh/freezed/freezed-3-x版本迁移工具.md'},
                            {'text': 'Freezed Class Tool Menu', 'link': 'zh/freezed/Freezed-Class-Tool-Menu.md'},
                            {'text': 'Json to Freezed', 'link': 'zh/freezed/Json-to-Freezed.md'},
                            {'text': '代码生成', 'link': 'zh/freezed/generate.md'}
                        ]
                    },
                    {
                        'text': 'Dart File',
                        'items': [
                            {'text': '资产文件路径检查功能', 'link': 'zh/dart-file/资产文件路径检查功能.md'},
                            {'text': '资产字符串快速打开文件', 'link': 'zh/dart-file/资产字符串快速打开文件.md'},
                            {'text': '资产图片预览功能', 'link': 'zh/dart-file/资产图片预览功能.md'},
                            {'text': 'Project Library Scan', 'link': 'zh/dart-file/Project-Library-scan.md'},
                            {'text': '参数类型内联显示', 'link': 'zh/dart-file/参数类型内联显示.md'}
                        ]
                    },
                    {
                        'text': 'Pubspec.yaml',
                        'items': [
                            {'text': '不再更新的三方包检测', 'link': 'zh/pubspec/不再更新的三方包检测.md'},
                            {'text': '第三方包工具', 'link': 'zh/pubspec/第三方包工具.md'}
                        ]
                    },
                    {
                        'text': '其他功能',
                        'items': [
                            {'text': '日志工具', 'link': 'zh/other/Log.md'},
                            {'text': 'Flutter新版本检测', 'link': 'zh/other/flutter新版本检测.md'},
                            {'text': 'L10n编辑器', 'link': 'zh/other/l10n-editor.md'},
                            {'text': 'Flutter 3.29.0 安卓迁移 Gradle 工具', 'link': 'zh/other/flutter3-29-0安卓迁移gradle工具.md'},
                            {'text': 'iOS 17 隐私扫描工具', 'link': 'zh/other/ios-17-隐私扫描工具.md'}
                        ]
                    },
                    {
                        'text': '资产管理',
                        'items': [
                            {'text': '资产预览窗口', 'link': 'zh/assets/资产预览窗口.md'},
                            {'text': '资产预览', 'link': 'zh/assets/资产预览.md'},
                            {'text': '资产生成类调用', 'link': 'zh/assets/资产生成类调用.md'}
                        ]
                    },
                    {
                        'text': '设置',
                        'items': [
                            {'text': '快速打开子目录文件夹', 'link': 'zh/settings/快速打开子目录文件夹.md'},
                            {'text': '链接', 'link': 'zh/settings/Links.md'},
                            {'text': '内联资产显示', 'link': 'zh/settings/内联资产显示.md'}
                        ]
                    },
                    {
                        'text': '其他',
                        'items': [
                            {'text': '打赏', 'link': 'zh/打赏.md'},
                            {'text': '更新日志', 'link': 'zh/更新日志.md'}
                        ]
                    }
                ]
            },
            'en': {
                'label': 'English',
                'items': [
                    {'text': 'Home', 'link': 'en/index.md'},
                    {
                        'text': 'Getting Started',
                        'items': [
                            {'text': 'Installation', 'link': 'en/installation.md'}
                        ]
                    },
                    {
                        'text': 'Dio',
                        'items': [
                            {'text': 'Dio Request Monitoring', 'link': 'en/dio/starter.md'},
                            {'text': 'Request Screenshot', 'link': 'en/dio/request-screenshot.md'}
                        ]
                    },
                    {
                        'text': 'Shared Preferences',
                        'items': [
                            {'text': 'Shared Preferences', 'link': 'en/shared_p/shared-preferences.md'}
                        ]
                    },
                    {
                        'text': 'Hive',
                        'items': [
                            {'text': 'Hive Cache Tool', 'link': 'en/hive/hive-cache-tool.md'}
                        ]
                    },
                    {
                        'text': 'Riverpod',
                        'items': [
                            {'text': 'Riverpod Settings', 'link': 'en/settings/riverpod.md'},
                            {'text': 'Riverpod Widget Tool', 'link': 'en/riverpod/riverpod-widget-tool.md'}
                        ]
                    },
                    {
                        'text': 'Freezed',
                        'items': [
                            {'text': 'Freezed 3.x Migration Tool', 'link': 'en/freezed/migration-tool.md'},
                            {'text': 'Json to Freezed', 'link': 'en/freezed/json-to-freezed.md'},
                            {'text': 'Code Generation', 'link': 'en/freezed/code-generation.md'},
                            {'text': 'Freezed Class Tool Menu', 'link': 'en/freezed/Freezed-Class-Tool-Menu.md'}
                        ]
                    },
                    {
                        'text': 'Dart File',
                        'items': [
                            {'text': 'Asset File Path Checking', 'link': 'en/dart-file/asset-path-checking.md'},
                            {'text': 'Quick Open Asset Files', 'link': 'en/dart-file/quick-open-asset-files.md'},
                            {'text': 'Asset Image Preview', 'link': 'en/dart-file/asset-image-preview.md'},
                            {'text': 'Project Library Scan', 'link': 'en/dart-file/project-library-scan.md'},
                            {'text': 'Parameter Type Inline Display', 'link': 'en/dart-file/parameter-type-inline-display.md'}
                        ]
                    },
                    {
                        'text': 'Pubspec.yaml',
                        'items': [
                            {'text': 'Outdated Package Detection', 'link': 'en/pubspec/outdated-package-detection.md'},
                            {'text': 'Third-party Package Tools', 'link': 'en/pubspec/third-party-package-tools.md'}
                        ]
                    },
                    {
                        'text': 'Other Features',
                        'items': [
                            {'text': 'Log Tools', 'link': 'en/other/log-tools.md'},
                            {'text': 'L10n Editor', 'link': 'en/other/l10n-editor.md'},
                            {'text': 'Flutter 3.29.0 Android Migration Gradle Tool', 'link': 'en/other/flutter-gradle-migration.md'},
                            {'text': 'iOS 17 Privacy Scanning Tool', 'link': 'en/other/ios-privacy-scanning.md'},
                            {'text': 'Flutter Version Detection', 'link': 'en/other/flutter-version-detection.md'}
                        ]
                    },
                    {
                        'text': 'Asset Management',
                        'items': [
                            {'text': 'Asset Preview Window', 'link': 'en/assets/asset-preview-window.md'},
                            {'text': 'Asset Preview', 'link': 'en/assets/asset-preview.md'},
                            {'text': 'Asset Generation Class', 'link': 'en/assets/asset-generation-class.md'}
                        ]
                    },
                    {
                        'text': 'Settings',
                        'items': [
                            {'text': 'Riverpod Settings', 'link': 'en/settings/riverpod.md'},
                            {'text': 'Quick Open Subdirectory', 'link': 'en/settings/quick-open-subdirectory.md'},
                            {'text': 'Links', 'link': 'en/settings/links.md'},
                            {'text': 'Inline Asset Display', 'link': 'en/settings/inline-asset-display.md'}
                        ]
                    },
                    {
                        'text': 'Others',
                        'items': [
                            {'text': 'Donate', 'link': 'en/donate.md'},
                            {'text': 'Changelog', 'link': 'en/changelog.md'}
                        ]
                    }
                ]
            },
            'ja': {
                'label': '日本語',
                'items': [
                    {'text': 'ホーム', 'link': 'ja/index.md'},
                    {
                        'text': 'はじめに',
                        'items': [
                            {'text': 'インストール', 'link': 'ja/安装.md'}
                        ]
                    },
                    {
                        'text': 'Dio',
                        'items': [
                            {'text': 'Dioリクエスト監視', 'link': 'ja/dio/Starter.md'},
                            {'text': 'リクエスト情報スクリーンショット', 'link': 'ja/dio/接口信息截图.md'}
                        ]
                    },
                    {
                        'text': 'Shared Preferences',
                        'items': [
                            {'text': 'Shared Preferences', 'link': 'ja/shared_p/Shared_preferences.md'}
                        ]
                    },
                    {
                        'text': 'Hive',
                        'items': [
                            {'text': 'Hiveキャッシュツール', 'link': 'ja/hive/Hive缓存工具.md'}
                        ]
                    },
                    {
                        'text': 'Riverpod',
                        'items': [
                            {'text': 'Riverpodウィジェットツール', 'link': 'ja/riverpod/Riverpod-Widget-Tool.md'},
                            {'text': 'Riverpod設定', 'link': 'ja/settings/riverpod.md'}
                        ]
                    },
                    {
                        'text': 'Freezed',
                        'items': [
                            {'text': 'Freezed 3.x移行ツール', 'link': 'ja/freezed/freezed-3-x版本迁移工具.md'},
                            {'text': 'JsonからFreezedへ', 'link': 'ja/freezed/json-to-freezed.md'},
                            {'text': 'コード生成', 'link': 'ja/freezed/generate.md'},
                            {'text': 'Freezedクラスツールメニュー', 'link': 'ja/freezed/Freezed-Class-Tool-Menu.md'}
                        ]
                    },
                    {
                        'text': 'Dartファイル',
                        'items': [
                            {'text': 'アセットファイルパスチェック機能', 'link': 'ja/dart-file/资产文件路径检查功能.md'},
                            {'text': 'アセット文字列クイックオープンファイル', 'link': 'ja/dart-file/资产字符串快速打开文件.md'},
                            {'text': 'アセット画像プレビュー機能', 'link': 'ja/dart-file/资产图片预览功能.md'},
                            {'text': 'プロジェクトライブラリスキャン', 'link': 'ja/dart-file/Project-Library-scan.md'},
                            {'text': 'パラメータ型インライン表示', 'link': 'ja/dart-file/参数类型内联显示.md'}
                        ]
                    },
                    {
                        'text': 'Pubspec.yaml',
                        'items': [
                            {'text': '更新されていないサードパーティパッケージの検出', 'link': 'ja/pubspec/不再更新的三方包检测.md'},
                            {'text': 'サードパーティパッケージツール', 'link': 'ja/pubspec/第三方包工具.md'}
                        ]
                    },
                    {
                        'text': 'その他の機能',
                        'items': [
                            {'text': 'ログツール', 'link': 'ja/other/Log.md'},
                            {'text': 'L10nエディタ', 'link': 'ja/other/l10n-editor.md'},
                            {'text': 'Flutter 3.29.0 Android Gradle移行ツール', 'link': 'ja/other/flutter3-29-0安卓迁移gradle工具.md'},
                            {'text': 'iOS 17プライバシースキャンツール', 'link': 'ja/other/ios-17-隐私扫描工具.md'},
                            {'text': 'Flutter新バージョン検出', 'link': 'ja/other/flutter新版本检测.md'}
                        ]
                    },
                    {
                        'text': 'アセット管理',
                        'items': [
                            {'text': 'アセットプレビューウィンドウ', 'link': 'ja/assets/资产预览窗口.md'},
                            {'text': 'アセットプレビュー', 'link': 'ja/assets/资产预览.md'},
                            {'text': 'アセット生成クラス呼び出し', 'link': 'ja/assets/资产生成类调用.md'}
                        ]
                    },
                    {
                        'text': '設定',
                        'items': [
                            {'text': 'Riverpod設定', 'link': 'ja/settings/riverpod.md'},
                            {'text': 'サブディレクトリクイックオープンフォルダ', 'link': 'ja/settings/快速打开子目录文件夹.md'},
                            {'text': 'リンク', 'link': 'ja/settings/Links.md'},
                            {'text': 'インラインアセット表示', 'link': 'ja/settings/内联资产显示.md'}
                        ]
                    },
                    {
                        'text': 'その他',
                        'items': [
                            {'text': '打赏', 'link': 'ja/打赏.md'},
                            {'text': '更新日志', 'link': 'ja/更新日志.md'}
                        ]
                    }
                ]
            }
        }
        
        return navigation
    
    def convert_to_mkdocs_format(self, navigation: Dict[str, Any]) -> List[Dict]:
        """Convert navigation structure to mkdocs format"""
        
        self.log("Converting to mkdocs navigation format...")
        
        mkdocs_nav = []
        
        # Add main homepage
        mkdocs_nav.append({'首页': 'index.md'})
        
        # Add each language section
        for lang_code, lang_data in navigation.items():
            lang_section = {lang_data['label']: self._convert_items(lang_data['items'])}
            mkdocs_nav.append(lang_section)
        
        return mkdocs_nav
    
    def _convert_items(self, items: List[Dict]) -> List[Dict]:
        """Convert navigation items to mkdocs format"""
        
        converted = []
        
        for item in items:
            if 'link' in item and 'items' not in item:
                # Simple link item
                converted.append({item['text']: item['link']})
            elif 'items' in item:
                # Section with sub-items
                sub_items = self._convert_items(item['items'])
                converted.append({item['text']: sub_items})
            else:
                # Text-only item
                converted.append(item['text'])
        
        return converted
    
    def update_mkdocs_config(self, mkdocs_nav: List[Dict]):
        """Update mkdocs.yml with new navigation"""
        
        self.log("Updating mkdocs.yml...")
        
        # Read current config
        with open(self.mkdocs_config_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find and replace the nav section
        nav_pattern = r'nav:\s*\[.*?\]'
        
        # Build new nav string
        nav_str = "nav:\n"
        for item in mkdocs_nav:
            nav_str += self._format_nav_item(item, indent=1)
        
        # Replace in content
        if re.search(nav_pattern, content, re.DOTALL):
            content = re.sub(nav_pattern, nav_str.rstrip(), content, flags=re.DOTALL)
        else:
            # Append nav section if not found
            content += "\n" + nav_str
        
        # Write back
        with open(self.mkdocs_config_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        self.log("✅ Updated mkdocs.yml with new navigation")
    
    def _format_nav_item(self, item: Any, indent: int = 0) -> str:
        """Format a navigation item for YAML"""
        
        prefix = "  " * indent
        
        if isinstance(item, dict):
            result = ""
            for key, value in item.items():
                if isinstance(value, str):
                    result += f"{prefix}- {key}: {value}\n"
                elif isinstance(value, list):
                    result += f"{prefix}- {key}:\n"
                    for sub_item in value:
                        result += self._format_nav_item(sub_item, indent + 1)
            return result
        else:
            return f"{prefix}- {item}\n"
    
    def run_build(self):
        """Run the navigation building process"""
        
        self.log("Building navigation for mkdocs...")
        
        try:
            # Build navigation structure
            navigation = self.build_navigation_structure()
            
            # Convert to mkdocs format
            mkdocs_nav = self.convert_to_mkdocs_format(navigation)
            
            # Update mkdocs config
            self.update_mkdocs_config(mkdocs_nav)
            
            self.log("✅ Navigation building completed successfully!")
            
        except Exception as e:
            self.log(f"❌ Navigation building failed: {str(e)}")
            raise

def main():
    """Main function"""
    
    mkdocs_config = "mkdocs.yml"
    
    if not Path(mkdocs_config).exists():
        print(f"❌ MkDocs config not found: {mkdocs_config}")
        return
    
    builder = NavigationBuilder(mkdocs_config)
    builder.run_build()

if __name__ == "__main__":
    main()