import * as path from "node:path";
import { defineConfig } from "rspress/config";

export default defineConfig({
  root: path.join(__dirname, "docs"),
  title: "FlutterX 插件文档",
  description: "FlutterX - Flutter开发者快速开发的辅助工具插件",
  icon: "/images/logo.svg",
  logo: {
    light: "/images/logo.svg",
    dark: "/images/logo.svg",
  },
  lang: "zh",
  build: {
    outDir: "doc_build",
  },
  themeConfig: {
    locales: [
      {
        lang: "en",
        label: "English",
        outlineTitle: "On This Page",
      },
      {
        lang: "zh",
        label: "简体中文",
        outlineTitle: "大纲",
      },
      {
        lang: "ja",
        label: "日本語",
        outlineTitle: "目次",
      },
    ],
    socialLinks: [
      {
        icon: "github",
        mode: "link",
        content: "https://github.com/mdddj/dd_flutter_idea_plugin",
      },
    ],
    nav: [
      {
        text: "首页",
        link: "/",
        activeMatch: "^/$"
      },
      {
        text: "文档",
        link: "/安装",
        activeMatch: "^/(安装$|zh|en|ja|dio/|shared_p/|hive/|riverpod/|freezed/|dart-file/|pubspec/|other/|assets/|settings/)"
      },
    ],
    sidebar: {
      "/": [
        {
          text: "开始使用",
          items: [
            {
              text: "安装",
              link: "/安装",
            },
          ],
        },
        {
          text: "Dio",
          items: [
            {
              text: "Dio接口监听",
              link: "/dio/Starter",
            },
            {
              text: "接口信息截图",
              link: "/dio/接口信息截图",
            },
          ],
        },
        {
          text: "Shared Preferences",
          items: [
            {
              text: "Shared Preferences",
              link: "/shared_p/Shared_preferences",
            },
          ],
        },
        {
          text: "Hive",
          items: [
            {
              text: "Hive缓存工具",
              link: "/hive/Hive缓存工具",
            },
          ],
        },
        {
          text: "Riverpod",
          items: [
            {
              text: "Riverpod Widget Tool",
              link: "/riverpod/Riverpod-Widget-Tool",
            },
          ],
        },
        {
          text: "Freezed",
          items: [
            {
              text: "Freezed 3.x版本迁移工具",
              link: "/freezed/freezed-3-x版本迁移工具",
            },
            {
              text: "Json to Freezed",
              link: "/freezed/Json-to-Freezed",
            },
            {
              text: "代码生成",
              link: "/freezed/generate",
            },
            {
              text: "Freezed Class Tool Menu",
              link: "/freezed/Freezed-Class-Tool-Menu",
            },
          ],
        },
        {
          text: "Dart File",
          items: [
            {
              text: "资产文件路径检查功能",
              link: "/dart-file/资产文件路径检查功能",
            },
            {
              text: "资产字符串快速打开文件",
              link: "/dart-file/资产字符串快速打开文件",
            },
            {
              text: "资产图片预览功能",
              link: "/dart-file/资产图片预览功能",
            },
            {
              text: "Project Library Scan",
              link: "/dart-file/Project-Library-scan",
            },
            {
              text: "参数类型内联显示",
              link: "/dart-file/参数类型内联显示",
            },
          ],
        },
        {
          text: "Pubspec.yaml",
          items: [
            {
              text: "不再更新的三方包检测",
              link: "/pubspec/不再更新的三方包检测",
            },
            {
              text: "第三方包工具",
              link: "/pubspec/第三方包工具",
            },
          ],
        },
        {
          text: "其他功能",
          items: [
            {
              text: "日志工具",
              link: "/other/Log",
            },
            {
              text: "L10n编辑器",
              link: "/other/l10n-editor",
            },
            {
              text: "Flutter 3.29.0 安卓迁移 Gradle 工具",
              link: "/other/flutter3-29-0安卓迁移gradle工具",
            },
            {
              text: "iOS 17 隐私扫描工具",
              link: "/other/ios-17-隐私扫描工具",
            },
            {
              text: "Flutter新版本检测",
              link: "/other/flutter新版本检测",
            },
          ],
        },
        {
          text: "资产管理",
          items: [
            {
              text: "资产预览窗口",
              link: "/assets/资产预览窗口",
            },
            {
              text: "资产预览",
              link: "/assets/资产预览",
            },
            {
              text: "资产生成类调用",
              link: "/assets/资产生成类调用",
            },
          ],
        },
        {
          text: "设置",
          items: [
            {
              text: "Riverpod设置",
              link: "/settings/riverpod",
            },
            {
              text: "快速打开子目录文件夹",
              link: "/settings/快速打开子目录文件夹",
            },
            {
              text: "链接",
              link: "/settings/Links",
            },
            {
              text: "内联资产显示",
              link: "/settings/内联资产显示",
            },
          ],
        },
        {
          text: "其他",
          items: [
            {
              text: "打赏",
              link: "/打赏",
            },
            {
              text: "更新日志",
              link: "/更新日志",
            },
          ],
        },
      ],
      "/en/": [
        {
          text: "Getting Started",
          items: [
            {
              text: "Installation",
              link: "/en/installation",
            },
          ],
        },
        {
          text: "Dio",
          items: [
            {
              text: "Dio Request Monitoring",
              link: "/en/dio/starter",
            },
            {
              text: "Request Information Screenshot",
              link: "/en/dio/request-screenshot",
            },
          ],
        },
        {
          text: "Shared Preferences",
          items: [
            {
              text: "Shared Preferences",
              link: "/en/shared_p/shared-preferences",
            },
          ],
        },
        {
          text: "Hive",
          items: [
            {
              text: "Hive Cache Tool",
              link: "/en/hive/hive-cache-tool",
            },
          ],
        },
        {
          text: "Riverpod",
          items: [
            {
              text: "Riverpod Widget Tool",
              link: "/en/riverpod/riverpod-widget-tool",
            },
          ],
        },
        {
          text: "Freezed",
          items: [
            {
              text: "Freezed 3.x Migration Tool",
              link: "/en/freezed/migration-tool",
            },
            {
              text: "Json to Freezed",
              link: "/en/freezed/json-to-freezed",
            },
            {
              text: "Code Generation",
              link: "/en/freezed/code-generation",
            },
            {
              text: "Freezed Class Tool Menu",
              link: "/en/freezed/class-tool-menu",
            },
          ],
        },
        {
          text: "Dart File",
          items: [
            {
              text: "Asset File Path Checking",
              link: "/en/dart-file/asset-path-checking",
            },
            {
              text: "Quick Open Asset Files",
              link: "/en/dart-file/quick-open-asset-files",
            },
            {
              text: "Asset Image Preview",
              link: "/en/dart-file/asset-image-preview",
            },
            {
              text: "Project Library Scan",
              link: "/en/dart-file/project-library-scan",
            },
            {
              text: "Parameter Type Inline Display",
              link: "/en/dart-file/parameter-type-inline-display",
            },
          ],
        },
        {
          text: "Pubspec.yaml",
          items: [
            {
              text: "Outdated Package Detection",
              link: "/en/pubspec/outdated-package-detection",
            },
            {
              text: "Third-party Package Tools",
              link: "/en/pubspec/third-party-package-tools",
            },
          ],
        },
        {
          text: "Other Features",
          items: [
            {
              text: "Log Tools",
              link: "/en/other/log-tools",
            },
            {
              text: "L10n Editor",
              link: "/en/other/l10n-editor",
            },
            {
              text: "Flutter 3.29.0 Android Migration Gradle Tool",
              link: "/en/other/flutter-gradle-migration",
            },
            {
              text: "iOS 17 Privacy Scanning Tool",
              link: "/en/other/ios-privacy-scanning",
            },
            {
              text: "Flutter Version Detection",
              link: "/en/other/flutter-version-detection",
            },
          ],
        },
        {
          text: "Asset Management",
          items: [
            {
              text: "Asset Preview Window",
              link: "/en/assets/asset-preview-window",
            },
            {
              text: "Asset Preview",
              link: "/en/assets/asset-preview",
            },
            {
              text: "Asset Generation Class",
              link: "/en/assets/asset-generation-class",
            },
          ],
        },
        {
          text: "Settings",
          items: [
            {
              text: "Riverpod Settings",
              link: "/en/settings/riverpod",
            },
            {
              text: "Quick Open Subdirectory",
              link: "/en/settings/quick-open-subdirectory",
            },
            {
              text: "Links",
              link: "/en/settings/links",
            },
            {
              text: "Inline Asset Display",
              link: "/en/settings/inline-asset-display",
            },
          ],
        },
        {
          text: "Others",
          items: [
            {
              text: "Donate",
              link: "/en/donate",
            },
            {
              text: "Changelog",
              link: "/en/changelog",
            },
          ],
        },
      ],
      "/ja/": [
        {
          text: "开始使用",
          items: [
            {
              text: "安装",
              link: "/ja/安装",
            },
          ],
        },
        {
          text: "Dio",
          items: [
            {
              text: "Dio接口监听",
              link: "/ja/dio/Starter",
            },
            {
              text: "接口信息截图",
              link: "/ja/dio/接口信息截图",
            },
          ],
        },
        {
          text: "Shared Preferences",
          items: [
            {
              text: "Shared Preferences",
              link: "/ja/shared_p/Shared_preferences",
            },
          ],
        },
        {
          text: "Hive",
          items: [
            {
              text: "Hive缓存工具",
              link: "/ja/hive/Hive缓存工具",
            },
          ],
        },
        {
          text: "Riverpod",
          items: [
            {
              text: "Riverpod Widget Tool",
              link: "/ja/riverpod/Riverpod-Widget-Tool",
            },
          ],
        },
        {
          text: "Freezed",
          items: [
            {
              text: "Freezed 3.x版本迁移工具",
              link: "/ja/freezed/freezed-3-x版本迁移工具",
            },
            {
              text: "Json to Freezed",
              link: "/ja/freezed/Json-to-Freezed",
            },
            {
              text: "代码生成",
              link: "/ja/freezed/generate",
            },
            {
              text: "Freezed Class Tool Menu",
              link: "/ja/freezed/Freezed-Class-Tool-Menu",
            },
          ],
        },
        {
          text: "Dart File",
          items: [
            {
              text: "资产文件路径检查功能",
              link: "/ja/dart-file/资产文件路径检查功能",
            },
            {
              text: "资产字符串快速打开文件",
              link: "/ja/dart-file/资产字符串快速打开文件",
            },
            {
              text: "资产图片预览功能",
              link: "/ja/dart-file/资产图片预览功能",
            },
            {
              text: "Project Library Scan",
              link: "/ja/dart-file/Project-Library-scan",
            },
            {
              text: "参数类型内联显示",
              link: "/ja/dart-file/参数类型内联显示",
            },
          ],
        },
        {
          text: "Pubspec.yaml",
          items: [
            {
              text: "不再更新的三方包检测",
              link: "/ja/pubspec/不再更新的三方包检测",
            },
            {
              text: "第三方包工具",
              link: "/ja/pubspec/第三方包工具",
            },
          ],
        },
        {
          text: "其他功能",
          items: [
            {
              text: "日志工具",
              link: "/ja/other/Log",
            },
            {
              text: "L10n编辑器",
              link: "/ja/other/l10n-editor",
            },
            {
              text: "Flutter 3.29.0 安卓迁移 Gradle 工具",
              link: "/ja/other/flutter3-29-0安卓迁移gradle工具",
            },
            {
              text: "iOS 17 隐私扫描工具",
              link: "/ja/other/ios-17-隐私扫描工具",
            },
            {
              text: "Flutter新版本检测",
              link: "/ja/other/flutter新版本检测",
            },
          ],
        },
        {
          text: "资产管理",
          items: [
            {
              text: "资产预览窗口",
              link: "/ja/assets/资产预览窗口",
            },
            {
              text: "资产预览",
              link: "/ja/assets/资产预览",
            },
            {
              text: "资产生成类调用",
              link: "/ja/assets/资产生成类调用",
            },
          ],
        },
        {
          text: "设置",
          items: [
            {
              text: "Riverpod设置",
              link: "/ja/settings/riverpod",
            },
            {
              text: "快速打开子目录文件夹",
              link: "/ja/settings/快速打开子目录文件夹",
            },
            {
              text: "链接",
              link: "/ja/settings/Links",
            },
            {
              text: "内联资产显示",
              link: "/ja/settings/内联资产显示",
            },
          ],
        },
        {
          text: "其他",
          items: [
            {
              text: "打赏",
              link: "/ja/打赏",
            },
            {
              text: "更新日志",
              link: "/ja/更新日志",
            },
          ],
        },
      ],
    },
  },
});
