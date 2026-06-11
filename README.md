# Antigravity IDE 汉化补丁

这是一个给本机 Antigravity IDE 使用的轻量汉化补丁工具。它采用本地注入方式，在 `workbench.html` 和 `workbench-jetski-agent.html` 中加载 `antigravity_zh_cn.js`，通过 DOM 文本替换汉化常见菜单、命令、设置和 Antigravity 专属入口。

## 当前定位

- 适配路径：`C:\Users\hongl\AppData\Local\Programs\Antigravity IDE`
- 已确认版本：Antigravity IDE `2.0.4`
- 已确认基线：VS Code `1.107.0`
- 方案类型：本地补丁，不是官方语言包

## 使用方式

查看状态：

```powershell
python .\antigravity_ide_hanhua.py status
```

安装汉化：

```powershell
python .\antigravity_ide_hanhua.py install
```

恢复原始文件：

```powershell
python .\antigravity_ide_hanhua.py restore
```

如果安装路径不同：

```powershell
python .\antigravity_ide_hanhua.py status --install-dir "D:\Tools\Antigravity IDE"
```

## 工作原理

脚本会做以下事情：

1. 备份 `workbench.html` 和 `product.json`，备份后缀为 `.agzh.bak`。
2. 备份 `workbench-jetski-agent.html`，这个入口承载 Antigravity 的 Settings 等专属界面。
3. 生成 `antigravity_zh_cn.js`。
4. 在 `workbench.html` 的 `workbench.js` 前注入汉化脚本。
5. 在 `workbench-jetski-agent.html` 的 `jetskiAgent.js` 前注入汉化脚本。
6. 重新计算两个 HTML 文件的 SHA256 校验值。
7. 更新 `product.json` 中对应的 `checksums` 记录。

## 风险说明

- 这是本地补丁，会修改 Antigravity IDE 安装目录。
- Antigravity IDE 更新后可能覆盖补丁，需要重新执行 `install`。
- 如果 IDE 启动异常，执行 `restore` 恢复。
- 当前是首版词典，优先覆盖常见入口和 Antigravity 专属命令，后续可以继续补充未翻译文本。
