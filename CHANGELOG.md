# 更新日志 (Changelog)

## [2026-06-15]
- **新增**：`antigravity_hanhua.py` 和 `antigravity_ide_hanhua.py` 现已原生支持 macOS 环境。
  - 自动识别当前操作系统（`sys.platform`），动态切换 Windows 和 macOS 专有路径。
  - 完美支持 macOS 默认安装路径 `/Applications/Antigravity.app/Contents` 和 `/Applications/Antigravity IDE.app/Contents`。
  - 修复了 macOS 环境下执行 `inject` 命令时，由于尝试访问 Windows 特定 `AppData` 目录导致报错找不到 `DevToolsActivePort` 端口文件的问题。现已适配为正确的 `~/Library/Application Support/Antigravity` 目录。
  - 修复了 IDE 补丁在 macOS 上无法正确识别 `Resources`（大写）目录结构的问题。
