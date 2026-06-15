# -*- coding: utf-8 -*-
"""Antigravity IDE 汉化补丁工具。

用法：
  python antigravity_hanhua.py status
  python antigravity_hanhua.py install
  python antigravity_hanhua.py restore
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import shutil
import sys
from pathlib import Path


if sys.platform == "darwin":
    默认安装目录 = Path("/Applications/Antigravity IDE.app/Contents")
else:
    默认安装目录 = Path(r"C:\Users\hongl\AppData\Local\Programs\Antigravity IDE")
注入标记 = "ANTIGRAVITY_ZH_CN_INJECTION"
脚本文件名 = "antigravity_zh_cn.js"
备份后缀 = ".agzh.bak"
HTML校验路径 = {
    "workbench": "vs/code/electron-browser/workbench/workbench.html",
    "jetski": "vs/code/electron-browser/workbench/workbench-jetski-agent.html",
}


def 计算校验值(文件路径: Path) -> str:
    摘要 = hashlib.sha256(文件路径.read_bytes()).digest()
    return base64.b64encode(摘要).decode("ascii").rstrip("=")


def 定位文件(安装目录: Path) -> dict[str, Path]:
    app目录 = 安装目录 / ("Resources" if sys.platform == "darwin" else "resources") / "app"
    workbench目录 = app目录 / "out" / "vs" / "code" / "electron-browser" / "workbench"
    文件 = {
        "product": app目录 / "product.json",
        "workbench": workbench目录 / "workbench.html",
        "jetski": workbench目录 / "workbench-jetski-agent.html",
        "js": workbench目录 / 脚本文件名,
    }
    缺失 = [str(路径) for 路径 in 文件.values() if 路径.name != 脚本文件名 and not 路径.exists()]
    if 缺失:
        raise FileNotFoundError("缺少必要文件：\n" + "\n".join(缺失))
    return 文件


def 读取文本(文件路径: Path) -> str:
    return 文件路径.read_text(encoding="utf-8")


def 写入文本(文件路径: Path, 内容: str) -> None:
    文件路径.write_text(内容, encoding="utf-8", newline="")


def 备份一次(文件路径: Path) -> Path:
    备份路径 = 文件路径.with_name(文件路径.name + 备份后缀)
    if not 备份路径.exists():
        shutil.copy2(文件路径, 备份路径)
    return 备份路径


def 生成汉化脚本() -> str:
    # 词典按“精准 UI 文本”优先，避免误改编辑器代码内容。
    词典 = {
        "Antigravity": "Antigravity",
        "Antigravity Editor": "Antigravity 编辑器",
        "Settings - Permissions": "设置 - 权限",
        "Settings - Account": "设置 - 账户",
        "Settings - Appearance": "设置 - 外观",
        "Settings - Notifications": "设置 - 通知",
        "Settings - Models": "设置 - 模型",
        "Settings - Customizations": "设置 - 自定义",
        "Settings - Browser": "设置 - 浏览器",
        "Settings - Tab": "设置 - 补全",
        "Settings - Editor": "设置 - 编辑器",
        "Agent": "智能体",
        "Agents": "智能体",
        "Agent security mode": "智能体安全模式",
        "Select one of the three options. Agent settings and permissions can be further customized below.": "请选择三种模式之一。智能体设置和权限可在下方继续自定义。",
        "Full access": "完全访问",
        "Agents have full access to your machine and external resources.": "智能体可以完全访问你的本机和外部资源。",
        "Sandboxed": "沙盒模式",
        "Agents run in a secure sandbox that restricts access to external resources outside of your trusted folders.": "智能体在安全沙盒中运行，会限制其访问可信文件夹之外的外部资源。",
        "Strict": "严格模式",
        "Terminal commands always require review and the agent cannot access files outside of its given workspaces.": "终端命令始终需要审核，并且智能体不能访问指定工作区之外的文件。",
        "Terminal Command Auto Execution": "终端命令自动执行",
        "Controls whether terminal commands require your approval before running.": "控制终端命令运行前是否需要你的批准。",
        "Note: A change to this setting will only apply to new messages sent to Agent. In-progress responses will use the previous setting value.": "注意：此设置的变更只会应用于发送给智能体的新消息。正在进行的回复仍会使用之前的设置值。",
        "Always Proceed": "始终继续",
        "Proceed in Sandbox": "在沙盒中继续",
        "Request Review": "请求审核",
        "Always Ask": "始终询问",
        "Enable Shell Integration": "启用 Shell 集成",
        "When enabled, Agent will use IDE's shell integration to detect and report terminal command execution.": "启用后，智能体会使用 IDE 的 Shell 集成来检测并报告终端命令执行。",
        "File Access": "文件访问",
        "Agent Non-Workspace File Access": "智能体非工作区文件访问",
        "Allows the agent to access files outside of your current workspace.": "允许智能体访问当前工作区之外的文件。",
        "Auto-Open Edited Files": "自动打开已编辑文件",
        "Open files in the background if Agent creates or edits them": "当智能体创建或编辑文件时，在后台打开这些文件",
        "Planning": "规划",
        "Code Review": "代码审查",
        "Artifact Review": "产物审查",
        "Explain and Fix": "解释并修复",
        "Explain and Fix in Current Conversation": "在当前对话中解释并修复",
        "Agent Auto-Fix Lints": "智能体自动修复 Lint",
        "When enabled, Agent is given awareness of lint errors created by its edits and may fix them without explicit user prompting.": "启用后，智能体会感知其编辑产生的 Lint 错误，并可在无需用户明确提示的情况下修复。",
        "Strict Mode": "严格模式",
        "When enabled, enforces settings that prevent the agent from autonomously running targeted exploits and requires human review for all agent actions. Visit antigravity.google/docs/strict-mode for details.": "启用后，会强制使用防止智能体自主运行定向利用的设置，并要求人工审核所有智能体操作。详情见 antigravity.google/docs/strict-mode。",
        "Enable Demo Mode (Beta)": "启用演示模式（测试）",
        "Enable Terminal Sandbox": "启用终端沙盒",
        "When enabled, terminal commands run with sandbox restrictions.": "启用后，终端命令会在沙盒限制下运行。",
        "Sandbox Allow Network": "沙盒允许网络访问",
        "When enabled, sandboxed commands are allowed to make network requests.": "启用后，沙盒命令可以发起网络请求。",
        "Allow List Terminal Commands": "终端命令允许列表",
        "Deny List Terminal Commands": "终端命令拒绝列表",
        "Agent auto-executes commands matched by an allow list entry.": "智能体会自动执行匹配允许列表条目的命令。",
        "Agent asks for permission before executing commands matched by a deny list entry.": "智能体在执行匹配拒绝列表条目的命令前会请求权限。",
        "Permissions": "权限",
        "Chat": "对话",
        "New Chat": "新建对话",
        "Open Chat": "打开对话",
        "Ask": "询问",
        "Ask Agent": "询问智能体",
        "Rules": "规则",
        "Rule Editor": "规则编辑器",
        "Workflow Editor": "工作流编辑器",
        "Workflow": "工作流",
        "Workflows": "工作流",
        "Skills": "技能",
        "Subagents": "子智能体",
        "MCP": "MCP",
        "Tools": "工具",
        "Browser": "浏览器",
        "Browser Allowlist": "浏览器白名单",
        "Enable Workspace API": "启用 Workspace API",
        "When enabled, Agent can interact with Google Workspace through the API to search and read documents.": "启用后，智能体可以通过 API 与 Google Workspace 交互以搜索和读取文档。",
        "Remote Control": "远程控制",
        "Enable Remote Control": "启用远程控制",
        "If enabled, you can manage your conversations from the Antigravity website. Please reload the application to apply this setting.": "启用后，你可以从 Antigravity 网站管理对话。请重新加载应用以应用此设置。",
        "Open Browser": "打开浏览器",
        "Show Browser Allowlist": "显示浏览器白名单",
        "Allowlist": "白名单",
        "Settings": "设置",
        "Import": "导入",
        "Import VS Code settings": "导入 VS Code 设置",
        "Import VS Code extensions": "导入 VS Code 扩展",
        "Import VS Code recent workspaces": "导入 VS Code 最近工作区",
        "Import Cursor settings": "导入 Cursor 设置",
        "Import Cursor extensions": "导入 Cursor 扩展",
        "Import Windsurf settings": "导入 Windsurf 设置",
        "Import Windsurf extensions": "导入 Windsurf 扩展",
        "Generate Commit Message": "生成提交信息",
        "Restart Language Server": "重启语言服务器",
        "Kill Language Server and Reload Window": "终止语言服务器并重载窗口",
        "Toggle Persistent Language Server and Reload Window": "切换常驻语言服务器并重载窗口",
        "Open Persistent Language Server Log": "打开常驻语言服务器日志",
        "Copy API Key to Clipboard": "复制 API Key 到剪贴板",
        "Open Changelog": "打开更新日志",
        "Log in to IDE": "登录 IDE",
        "Provide Auth Token (Backup Login)": "提供认证令牌（备用登录）",
        "[Beta] Start Demo Mode": "[测试] 启动演示模式",
        "[Beta] End Demo Mode": "[测试] 结束演示模式",
        "General": "通用",
        "Manage your plan, credentials, and general preferences.": "管理你的套餐、凭据和通用偏好设置。",
        "Enable Telemetry": "启用遥测",
        "Marketing Emails": "营销邮件",
        "Email": "邮箱",
        "Not Signed In": "未登录",
        "Your Plan": "你的套餐",
        "Upgrade": "升级",
        "Terms of Service": "服务条款",
        "Privacy": "隐私",
        "Account": "账户",
        "Appearance": "外观",
        "Notifications": "通知",
        "Models": "模型",
        "Customizations": "自定义",
        "Tab": "补全",
        "Editor": "编辑器",
        "Workspaces": "工作区",
        "Shortcuts": "快捷键",
        "Provide Feedback": "提供反馈",
        "Global": "全局",
        "Project": "项目",
        "Custom Agents": "自定义智能体",
        "No customizations found for this workspace.": "此工作区未找到自定义配置。",
        "Loading workspace customizations...": "正在加载工作区自定义配置...",
        "Build with Antigravity Plugins": "使用 Antigravity 插件构建",
        "Plugins": "插件",
        "Plugin": "插件",
        "No Plugins Available": "没有可用插件",
        "Refreshing...": "正在刷新...",
        "Downloading...": "正在下载...",
        "Deleting...": "正在删除...",
        "Download": "下载",
        "Copy path": "复制路径",
        "Path copied!": "路径已复制！",
        "Edit config": "编辑配置",
        "Delete agent": "删除智能体",
        "Search MCP servers": "搜索 MCP 服务器",
        "MCP Servers": "MCP 服务器",
        "No MCP servers configured.": "尚未配置 MCP 服务器。",
        "Install MCP Server": "安装 MCP 服务器",
        "Paste auth code": "粘贴授权码",
        "Submit": "提交",
        "Loading plugins...": "正在加载插件...",
        "Plugin Operation Error:": "插件操作错误：",
        "Login": "登录",
        "Log In": "登录",
        "Sign In": "登录",
        "Logout": "退出登录",
        "Log Out": "退出登录",
        "Sign Out": "退出登录",
        "Extensions": "扩展",
        "Marketplace": "市场",
        "Search": "搜索",
        "Source Control": "源代码管理",
        "Run and Debug": "运行和调试",
        "Explorer": "资源管理器",
        "Problems": "问题",
        "Output": "输出",
        "Terminal": "终端",
        "Command Palette": "命令面板",
        "Preferences": "首选项",
        "Keyboard Shortcuts": "键盘快捷键",
        "User": "用户",
        "Workspace": "工作区",
        "Remote": "远程",
        "Open Folder": "打开文件夹",
        "Open File": "打开文件",
        "New File": "新建文件",
        "New Folder": "新建文件夹",
        "Save": "保存",
        "Save All": "全部保存",
        "Close": "关闭",
        "Cancel": "取消",
        "OK": "确定",
        "Yes": "是",
        "No": "否",
        "Retry": "重试",
        "Refresh": "刷新",
        "Reload": "重载",
        "Continue": "继续",
        "New Conversation": "新建对话",
        "Past Conversations": "历史对话",
        "Additional Options": "附加选项",
        "Customization": "自定义",
        "Record Audio": "录制音频",
        "Auto Execution": "自动执行",
        "Manage": "管理",
        "Snooze": "暂停",
        "Start": "开始",
        "On": "开启",
        "Off": "关闭",
        "Back": "返回",
        "Next": "下一步",
        "Previous": "上一步",
        "Agent Decides": "由智能体决定",
        "Trust the agent to do tasks end-to-end": "信任智能体端到端地完成任务",
        "Assist the agent to complete tasks": "协助智能体完成任务",
        "Collaborate with the agent to complete tasks": "与智能体协作完成任务",
        "Show AI autocomplete suggestions in the editor": "在编辑器中显示 AI 自动补全建议",
        "Predict the location of your next edit and navigates you there with a tab keypress": "预测你的下一次编辑位置，并通过按下 Tab 键导航到该处",
        "View all Antigravity IDE shortcuts": "查看所有 Antigravity IDE 快捷键",
        "Reset to default shortcuts": "恢复默认快捷键",
        "Enable": "启用",
        "Disable": "禁用",
        "Enabled": "已启用",
        "Disabled": "已禁用",
        "Install": "安装",
        "Uninstall": "卸载",
        "Update": "更新",
        "Restart": "重启",
        "Accept": "接受",
        "Reject": "拒绝",
        "Apply": "应用",
        "Discard": "放弃",
        "Delete": "删除",
        "Remove": "移除",
        "Add": "添加",
        "Edit": "编辑",
        "Done": "完成",
        "Loading": "加载中",
        "Error": "错误",
        "Warning": "警告",
        "Info": "信息",
        "Automation": "自动化",
        "History": "历史",
        "When toggled on, Antigravity IDE collects usage data to help Google enhance performance and features.": "启用后，Antigravity IDE 会收集使用数据，帮助 Google 改进性能和功能。",
        "Receive product updates, tips, and promotions from Google Antigravity IDE via email.": "通过邮件接收 Google Antigravity IDE 的产品更新、技巧和推广信息。",
        "You can upgrade to a Google AI Ultra plan to receive higher rate limits.": "你可以升级到 Google AI Ultra 套餐以获得更高的速率限制。",
        "By using this app, you agree to its": "使用此应用即表示你同意其",
        "Review Policy": "审核策略",
        "Specifies the agent's behavior when asking for review on artifacts, which are documents it creates to enable a richer conversation experience.": "指定智能体在请求审核产物时的行为。产物是智能体创建的文档，用于提供更丰富的对话体验。",
        "Conversation History": "对话历史",
        "When enabled, the agent will be able to access past conversations to inform its responses.": "启用后，智能体可以访问历史对话来辅助生成回复。",
        "Knowledge": "知识",
        "When enabled, the agent will be able to access its knowledge base to inform its responses and automatically generate knowledge items in the background.": "启用后，智能体可以访问其知识库来辅助生成回复，并在后台自动生成知识条目。",
        "Enable Sounds for Agent": "启用智能体声音",
        "When enabled, Antigravity will play a sound when Agent finishes generating a response.": "启用后，当智能体完成回复生成时，Antigravity 会播放提示音。",
        "Auto-Expand Changes Overview": "自动展开变更概览",
        "When enabled, the Changes Overview toolbar will automatically expand when Agent finishes generating a response.": "启用后，当智能体完成回复生成时，变更概览工具栏会自动展开。",
        "[Dev] GCP Project ID": "[开发] GCP 项目 ID",
        "GCP Project ID for enterprise features.": "企业功能使用的 GCP 项目 ID。",
        "Advanced Settings": "高级设置",
        "Advanced": "高级",
        "Advanced File Access": "高级文件访问",
        "Advanced Command Access": "高级命令访问",
        "Advanced Web Access": "高级网页访问",
        "Read Files": "读取文件",
        "Paths the agent can read.": "智能体可以读取的路径。",
        "Write Files": "写入文件",
        "Paths the agent can modify.": "智能体可以修改的路径。",
        "Commands": "命令",
        "Commands the agent can execute.": "智能体可以执行的命令。",
        "Commands Outside Sandbox": "沙盒外命令",
        "Commands the agent can run outside the sandbox.": "智能体可以在沙盒外运行的命令。",
        "MCP Tools": "MCP 工具",
        "External tools the agent can call via Model Context Protocol.": "智能体可通过 Model Context Protocol 调用的外部工具。",
        "Read URLs": "读取 URL",
        "URLs the agent can read or open in the browser.": "智能体可以在浏览器中读取或打开的 URL。",
        "Execute URLs": "执行 URL",
        "URLs the agent can actuate on using the browser.": "智能体可以通过浏览器执行操作的 URL。",
        "Configure the agent's visual theme and display preferences.": "配置智能体的视觉主题和显示偏好。",
        "Chat Settings": "对话设置",
        "Verbose agent chat": "显示详细智能体对话",
        "Display and preserve intermediate thinking steps": "显示并保留中间思考步骤",
        "Manage your notification preferences.": "管理你的通知偏好设置。",
        "Notification Settings": "通知设置",
        "To modify notification settings, open your operating system's system preferences.": "要修改通知设置，请打开操作系统的系统首选项。",
        "Open System Preferences": "打开系统首选项",
        "Configure AI models and view your quota.": "配置 AI 模型并查看你的配额。",
        "Model Credits": "模型点数",
        "Enable AI Credit Overages": "启用 AI 点数超额使用",
        "When toggled on, Antigravity IDE will use your AI credits to fulfill model requests once you're out of model quota. Antigravity IDE will always use your model quota first before using AI credits.": "启用后，当模型配额用尽时，Antigravity IDE 会使用你的 AI 点数来完成模型请求。Antigravity IDE 始终会先使用模型配额，再使用 AI 点数。",
        "Model Quota": "模型配额",
        "View your available model quota and AI credits. Model quota refreshes periodically based on your plan. Enable AI Credit Overages to continue using models when your quota is exhausted.": "查看可用模型配额和 AI 点数。模型配额会根据你的套餐定期刷新。启用 AI 点数超额使用后，配额耗尽时仍可继续使用模型。",
        "Refreshes in": "刷新于",
        "Configure default behaviors, skills, and MCP servers.": "配置默认行为、技能和 MCP 服务器。",
        "Token Usage": "Token 用量",
        "The breakdown below shows token usage from customizations like skills, rules, and MCP.": "下方明细显示技能、规则和 MCP 等自定义配置的 Token 用量。",
        "If the budget is exceeded, large customizations will be truncated automatically.": "如果超出预算，大型自定义配置将被自动截断。",
        "of the customization budget is available.": "的自定义预算可用。",
        "Show 1 breakdown": "显示 1 项明细",
        "Installed MCP Servers": "已安装的 MCP 服务器",
        "Add MCP": "添加 MCP",
        "Open MCP Config": "打开 MCP 配置",
        "No MCP Servers": "没有 MCP 服务器",
        "You currently don't have any MCP servers installed. Add an MCP server above or add a custom one via the MCP Config.": "你当前没有安装任何 MCP 服务器。可在上方添加 MCP 服务器，或通过 MCP 配置添加自定义服务器。",
        "You currently don't have any MCP 服务器 installed. Add an MCP server above or add a custom one via the MCP Config.": "你当前没有安装任何 MCP 服务器。可在上方添加 MCP 服务器，或通过 MCP 配置添加自定义服务器。",
        "Build With Google Plugins": "Build With Google 插件",
        "Build With Google Plugin": "Build With Google 插件",
        "Customize": "自定义",
        "Browser Settings": "浏览器设置",
        "Configure the browser subagent. It requires Google Chrome to be installed.": "配置浏览器子智能体。需要安装 Google Chrome。",
        "Configure the browser subagent. It requires": "配置浏览器子智能体。需要安装",
        "to be installed.": "。",
        "Enable Browser Tools": "启用浏览器工具",
        "When enabled, Agent can use browser tools to open URLs, read web pages, and interact with browser content. This allows the Agent to leverage Google Search for realtime knowledge and methods of validation, but any browser integration does increase exposure to external malicious parties for security exploits.": "启用后，智能体可以使用浏览器工具打开 URL、读取网页并与浏览器内容交互。这让智能体能够利用 Google 搜索获取实时知识和验证方法，但任何浏览器集成都可能增加暴露给外部恶意方进行安全利用的风险。",
        "Browser Javascript Execution Policy": "浏览器 JavaScript 执行策略",
        "Controls whether the agent can run custom JavaScript to automate complex browser actions.": "控制智能体是否可以运行自定义 JavaScript 来自动化复杂浏览器操作。",
        "Actuation Permissions": "执行权限",
        "Browser Actuation Rules": "浏览器执行规则",
        "Configure allowed and denied URLs for browser actuation.": "配置允许和拒绝浏览器执行操作的 URL。",
        "Suggestions": "建议",
        "Suggestions in Editor": "编辑器中的建议",
        "Show suggestions when typing in the editor": "在编辑器输入时显示建议",
        "Tab Speed": "Tab 速度",
        "Set the speed of tab suggestions": "设置 Tab 建议速度",
        "Highlight After Accept": "接受后高亮",
        "Highlight newly inserted text after accepting a Tab completion.": "接受 Tab 补全后高亮新插入的文本。",
        "Tab to Import": "Tab 导入",
        "Quickly add and update imports with a tab keypress.": "按 Tab 快速添加和更新导入。",
        "Navigation": "导航",
        "Tab to Jump": "Tab 跳转",
        "Predict the location of your next edit and navigates you there with a tab keypress.": "预测下一处编辑位置，并通过 Tab 键跳转过去。",
        "Context": "上下文",
        "Tab Gitignore Access": "Tab 访问 Gitignore",
        "Allow Tab to view and edit the files in .gitignore. Use with caution if your .gitignore lists files containing credentials, secrets, or other sensitive information.": "允许 Tab 查看和编辑 .gitignore 中的文件。如果 .gitignore 列出了包含凭据、密钥或其他敏感信息的文件，请谨慎使用。",
        "Editor Settings": "编辑器设置",
        "Configure editor-specific behaviors and shortcuts.": "配置编辑器专属行为和快捷键。",
        "Marketplace": "市场",
        "Marketplace Item URL": "市场项目 URL",
        "Marketplace Gallery URL": "市场 Gallery URL",
        "Changes the base URL on each extension page. You must restart Antigravity IDE to use the new marketplace after changing this value.": "更改每个扩展页面的基础 URL。修改后必须重启 Antigravity IDE 才能使用新的市场。",
        "Changes the base URL for marketplace search results. You must restart Antigravity IDE to use the new marketplace after changing this value.": "更改市场搜索结果的基础 URL。修改后必须重启 Antigravity IDE 才能使用新的市场。",
        "Selection Actions": "选择操作",
        "Show Selection Actions": "显示选择操作",
        "Show \"Edit\" and \"Chat\" buttons when selecting text in the editor.": "在编辑器中选择文本时显示“编辑”和“对话”按钮。",
        "To modify editor settings, open Settings within the editor window.": "要修改编辑器设置，请在编辑器窗口中打开设置。",
        "Open Editor Settings": "打开编辑器设置",
        "Fast": "快速",
        "Slow": "慢速",
        "Disabled": "已禁用",
        "Allow": "允许",
        "Deny list": "拒绝列表",
        "Allow list": "允许列表",
        "Agent never asks for confirmation before executing terminal commands (except those in the deny list). This provides the agent with the maximum ability to operate over long periods without intervention, but also has the highest risk of an agent executing an unsafe terminal command.": "智能体在执行终端命令前不会请求确认（拒绝列表中的命令除外）。这让智能体具备最长时间自主运行的最大能力，但也带来最高风险，可能执行不安全的终端命令。",
        "Agent never asks for confirmation before executing terminal commands (except those in the 拒绝 list). This provides the 智能体 with the maximum ability to operate over long periods without intervention, but also has the highest risk of an 智能体 executing an unsafe terminal command.": "智能体在执行终端命令前不会请求确认（拒绝列表中的命令除外）。这让智能体具备最长时间自主运行的最大能力，但也带来最高风险，可能执行不安全的终端命令。",
        "Agent always asks for confirmation before executing terminal commands (except those in the allow list).": "智能体在执行终端命令前始终请求确认（允许列表中的命令除外）。",
        "Agent always asks for confirmation before executing terminal commands (except those in the 允许 list).": "智能体在执行终端命令前始终请求确认（允许列表中的命令除外）。",
        "Deny": "拒绝",
        "Ask": "询问",
        "Agent's": "智能体的",
        "agent's": "智能体的",
        "Select one of the three options.": "请选择三种模式之一。",
        "Select one of the three options": "请选择三种模式之一",
        "Select one of the three options. 智能体设置和权限可在下方继续自定义。": "请选择三种模式之一。智能体设置和权限可在下方继续自定义。",
        "and permissions can be further customized below.": "和权限可在下方继续自定义。",
        "Agent settings and permissions can be further customized below.": "智能体设置和权限可在下方继续自定义。",
        "settings and permissions can be further customized below.": "设置和权限可在下方继续自定义。",
        "Select one of the three options. 智能体设置 and permissions can be further customized below.": "请选择三种模式之一。智能体设置和权限可在下方继续自定义。",
        "Specifies 智能体的 behavior when asking for review on artifacts, which are documents it creates to enable a richer conversation experience.": "指定智能体在请求审核产物时的行为。产物是智能体创建的文档，用于提供更丰富的对话体验。",
        "When enabled, 解释并修复 actions will continue in the current conversation instead of starting a new one.": "启用后，“解释并修复”操作会在当前对话中继续，而不是开启新对话。",
        "When enabled, '解释并修复' actions will continue in the current conversation instead of starting a new one.": "启用后，“解释并修复”操作会在当前对话中继续，而不是开启新对话。",
        "When enabled, Explain and Fix actions will continue in the current conversation instead of starting a new one.": "启用后，“解释并修复”操作会在当前对话中继续，而不是开启新对话。",
        "When enabled, 智能体 is given awareness of Lint errors created by its edits and may fix them without explicit user prompting.": "启用后，智能体会感知其编辑产生的 Lint 错误，并可在无需用户明确提示的情况下修复。",
        "When enabled, your UI will be slightly modified to ensure more consistent demos. This is only recommended for demo purposes. In most cases, you can run \"Antigravity: Start Demo Mode\" and \"Antigravity: Stop Demo Mode\" to control this switch and update your ~/.gemini/antigravity data directory.": "启用后，界面会略作调整，以确保演示效果更一致。此功能仅建议用于演示。大多数情况下，你可以运行“Antigravity: Start Demo Mode”和“Antigravity: Stop Demo Mode”来控制此开关，并更新 ~/.gemini/antigravity 数据目录。",
        "When enabled, your UI will be slightly modified to ensure more consistent demos. This is only recommended for demo purposes. In most cases, you can run \"Antigravity: Start 演示模式\" and \"Antigravity: Stop Demo Mode\" to control this switch and update your ~/.gemini/antigravity data directory.": "启用后，界面会略作调整，以确保演示效果更一致。此功能仅建议用于演示。大多数情况下，你可以运行“Antigravity: Start Demo Mode”和“Antigravity: Stop Demo Mode”来控制此开关，并更新 ~/.gemini/antigravity 数据目录。",
        "When enabled, 智能体 can use browser tools to open URL, read web pages, and interact with browser content. This allows the 智能体 to leverage Google Search for realtime knowledge and methods of validation, but any browser integration does increase exposure to external malicious parties for security exploits.": "启用后，智能体可以使用浏览器工具打开 URL、读取网页并与浏览器内容交互。这让智能体能够利用 Google 搜索获取实时知识和验证方法，但任何浏览器集成都可能增加暴露给外部恶意方进行安全利用的风险。",
        "Open Agent panel on window reload": "窗口重载时打开智能体面板",
        "Open agent panel on window reload": "窗口重载时打开智能体面板",
        "Open Agent Panel On Window Reload": "窗口重载时打开智能体面板",
        "When enabled, Agent panel will open on window reload.": "启用后，窗口重载时会打开智能体面板。",
        "When enabled, the agent panel will open on window reload.": "启用后，窗口重载时会打开智能体面板。",
        "For Unix shells, an allow list entry matches a command if its space-separated tokens form a prefix of the command's tokens. For PowerShell, the entry tokens may match any contiguous subsequence of the command tokens.": "对于 Unix shell，允许列表条目会在其空格分隔的 token 构成命令 token 前缀时匹配该命令。对于 PowerShell，条目 token 可匹配命令 token 的任意连续子序列。",
        "The deny list follows the same matching rules as the allow list and takes precedence over the allow list.": "拒绝列表遵循与允许列表相同的匹配规则，并优先于允许列表。",
        "Terminal commands the agent can execute.": "智能体可以执行的终端命令。",
        "Commands the agent can execute.": "智能体可以执行的命令。",
        "The agent can execute.": "智能体可以执行。",
        "the agent can execute.": "智能体可以执行。",
        "External tools the agent can call via Model Context Protocol.": "智能体可以通过 Model Context Protocol 调用的外部工具。",
        "URLs the agent can read or open in the browser.": "智能体可以在浏览器中读取或打开的 URL。",
        "URLs the agent can actuate on using the browser.": "智能体可以通过浏览器执行操作的 URL。",
        "Allows the agent to access files outside of your current workspace.": "允许智能体访问当前工作区之外的文件。",
        "Paths the agent can read.": "智能体可以读取的路径。",
        "Paths the agent can modify.": "智能体可以修改的路径。",
    }
    return f"""/* {注入标记}
 * Antigravity IDE 汉化脚本，由 antigravity_ide_hanhua.py 生成。
 */
(function () {{
  'use strict';

  const fanYiCiDian = new Map({json.dumps(list(词典.items()), ensure_ascii=False, indent=2)});

  function shiYingWenZiFu(ziFu) {{
    return !!ziFu && /[A-Za-z0-9]/.test(ziFu);
  }}

  function tiHuanDuanYu(yuanWen, yingWen, zhongWen) {{
    let jieGuo = '';
    let qiDian = 0;
    let weiZhi = yuanWen.indexOf(yingWen, qiDian);
    while (weiZhi !== -1) {{
      const qian = yuanWen[weiZhi - 1] || '';
      const hou = yuanWen[weiZhi + yingWen.length] || '';
      const qianXuYaoBianJie = /^[A-Za-z0-9]/.test(yingWen);
      const houXuYaoBianJie = /[A-Za-z0-9]$/.test(yingWen);
      const bianJieHeFa = (!qianXuYaoBianJie || !shiYingWenZiFu(qian)) && (!houXuYaoBianJie || !shiYingWenZiFu(hou));
      jieGuo += yuanWen.slice(qiDian, weiZhi);
      if (bianJieHeFa) {{
        jieGuo += zhongWen;
      }} else {{
        jieGuo += yingWen;
      }}
      qiDian = weiZhi + yingWen.length;
      weiZhi = yuanWen.indexOf(yingWen, qiDian);
    }}
    return jieGuo + yuanWen.slice(qiDian);
  }}

  const moShiCiDian = [
    [/^Search (.+)$/i, '搜索 $1'],
    [/^Open (.+)$/i, '打开 $1'],
    [/^Close (.+)$/i, '关闭 $1'],
    [/^Import (.+)$/i, '导入 $1'],
    [/^(.+) Settings$/i, '$1 设置'],
    [/^(\\d+) files?$/i, '$1 个文件'],
    [/^(\\d+) results?$/i, '$1 个结果'],
    [/^(\\d+) errors?$/i, '$1 个错误'],
    [/^(\\d+) warnings?$/i, '$1 个警告'],
    [/^Allow$/i, '允许'],
    [/^Deny$/i, '拒绝'],
    [/^Ask$/i, '询问']
  ];

  const tiaoGuoBiaoQian = new Set(['SCRIPT', 'STYLE', 'TEXTAREA', 'INPUT', 'CODE', 'PRE']);
  const tiaoGuoXuanZeQi = '.monaco-editor, .xterm, [contenteditable="true"]';

  function fanYiWenBen(yuanWen) {{
    if (!yuanWen) return yuanWen;
    const qian = yuanWen.match(/^\\s*/)[0];
    const hou = yuanWen.match(/\\s*$/)[0];
    const zhuTi = yuanWen.trim();
    if (!zhuTi) return yuanWen;
    let jieGuo = fanYiCiDian.get(zhuTi);
    if (!jieGuo) {{
      for (const [moShi, tiHuan] of moShiCiDian) {{
        if (moShi.test(zhuTi)) {{
          jieGuo = zhuTi.replace(moShi, tiHuan);
          break;
        }}
      }}
    }}
    if (!jieGuo) {{
      jieGuo = zhuTi;
      const pianDuan = Array.from(fanYiCiDian.entries()).sort((a, b) => b[0].length - a[0].length);
      for (const [yingWen, zhongWen] of pianDuan) {{
        if (yingWen.length < 4 || !jieGuo.includes(yingWen)) continue;
        jieGuo = tiHuanDuanYu(jieGuo, yingWen, zhongWen);
      }}
      jieGuo = fanYiCiDian.get(jieGuo) || jieGuo;
    }}
    let houChuLi = jieGuo || zhuTi;
    const zhengZeTiHuan = [
        [/^Select one of the\s*$/gi, "请选择"],
        [/^\s*options\.\s*(?:智能体)?(?:设置)?(?:\s*and\s*)?permissions\s+can\s+be\s+further\s+customized\s+below\.?/gi, "种安全模式。智能体设置和权限可在下方继续自定义。"],
        [/Select\W+one\W+of\W+the\W+three\W+options\.?/gi, "请选择三种模式之一。"],
        [/(?:智能体)?(?:设置)?(?:\s*and\s*)?permissions\s+can\s+be\s+further\s+customized\s+below\.?/gi, "智能体设置和权限可在下方继续自定义。"],
        [/Note that this may increase/gi, "请注意，这可能会增加"],
        [/tool usage\.?/gi, "的工具使用频率。"],
        [/never asks for confirmation before executing terminal commands \(except those in the/gi, "在执行终端命令前从不请求确认（除了位于"],
        [/always asks for confirmation before executing terminal commands \(except those in the/gi, "在执行终端命令前始终请求确认（除了位于"],
        [/List\)/gi, "列表中的命令）"],
        [/list\)/gi, "列表中的命令）"],
        [/are packaged collections of skills and MCPs to help the/gi, "是将技能和 MCP 打包的集合，用于帮助"],
        [/in Antigravity IDE work with Google developer products[\s\S]*?You can always change your choices in/gi, "在 Antigravity IDE 中使用 Google 开发者产品。你随时可以在"],
        [/(?:自定义)?\s*(?:智能体)?\s*to get a better, more personalized experience\.?/gi, "以获得更好、更个性化的体验。"],
        [/Learn more\.?/gi, "了解更多。"],
        [/(?:规则)?\s*help guide the behavior of\s*(?:智能体)?\.?/gi, "有助于指导智能体的行为。"],
        [/(?:工作流)?\s*are saved prompts that\s*(?:智能体)?\s*can follow\.?/gi, "是智能体可以遵循的已保存提示。"],
        [/To trigger a workflow, type "\/" in\s*(?:智能体)?\.?/gi, "要在智能体中触发工作流，请键入“/”。"]
    ];
    for (const [zz, th] of zhengZeTiHuan) {{
        houChuLi = houChuLi.replace(zz, th);
    }}
    houChuLi = houChuLi
        .replaceAll("拒绝 list", "拒绝列表")
        .replaceAll("允许 list", "允许列表")
        .replaceAll("This provides the 智能体 with the maximum ability to operate over long periods without intervention, but also has the highest risk of an 智能体 executing an unsafe terminal command.", "这让智能体具备最长时间自主运行的最大能力，但也带来最高风险，可能执行不安全的终端命令。")
        .replaceAll("Agent never asks for confirmation before executing terminal commands (except those in the 拒绝列表).", "智能体在执行终端命令前不会请求确认（拒绝列表中的命令除外）。")
        .replaceAll("智能体 never asks for confirmation before executing terminal commands (except those in the 拒绝列表).", "智能体在执行终端命令前不会请求确认（拒绝列表中的命令除外）。")
        .replaceAll("Agent always asks for confirmation before executing terminal commands (except those in the 允许列表).", "智能体在执行终端命令前始终请求确认（允许列表中的命令除外）。")
        .replaceAll("智能体 always asks for confirmation before executing terminal commands (except those in the 允许列表).", "智能体在执行终端命令前始终请求确认（允许列表中的命令除外）。")
        .replaceAll("Command automatically proceeds if the command runs inside the sandbox. Otherwise, it requests review.", "如果命令在沙盒内运行，则自动继续；否则请求审核。")
        .replaceAll("终端 command automatically proceeds if the command runs inside the sandbox. Otherwise, it requests review.", "如果命令在沙盒内运行，则自动继续；否则请求审核。")
        .replaceAll("When enabled, 智能体 can use browser tools to open URL, read web pages, and interact with browser content. This allows the 智能体 access to important (and often critical) knowledge and methods of validation, but any browser integration does increase exposure to external malicious parties for security exploits.", "启用后，智能体可以使用浏览器工具打开 URL、读取网页并与浏览器内容交互。这让智能体能够访问重要且通常关键的知识和验证方法，但任何浏览器集成都可能增加暴露给外部恶意方进行安全利用的风险。")
        .replaceAll("When enabled, 智能体 can use browser tools to open URL, read web pages, and interact with browser content. This allows the 智能体 to leverage Google Search for realtime knowledge and methods of validation, but any browser integration does increase exposure to external malicious parties for security exploits.", "启用后，智能体可以使用浏览器工具打开 URL、读取网页并与浏览器内容交互。这让智能体能够利用 Google 搜索获取实时知识和验证方法，但任何浏览器集成都可能增加暴露给外部恶意方进行安全利用的风险。")
        .replaceAll("When enabled, '解释并修复' actions will continue in the current conversation instead of starting a new one.", "启用后，“解释并修复”操作会在当前对话中继续，而不是开启新对话。")
        .replaceAll("智能体 never asks for review. This maximizes the autonomy of the 智能体, but also has the highest risk of the 智能体 operating over unsafe or injected Artifact content.", "智能体从不请求审核。这让智能体具备最大程度的自主权，但也带来针对不安全或被注入的产物内容进行操作的最高风险。")
        .replaceAll("Agent never asks for review. This maximizes the autonomy of the agent, but also has the highest risk of the agent operating over unsafe or injected Artifact content.", "智能体从不请求审核。这让智能体具备最大程度的自主权，但也带来针对不安全或被注入的产物内容进行操作的最高风险。")
        .replaceAll("智能体 always asks for review.", "智能体始终请求审核。")
        .replaceAll("Agent always asks for review.", "智能体始终请求审核。")
        .replaceAll("智能体 will always ask to review in strict mode.", "在严格模式下，智能体将始终请求审核。")
        .replaceAll("Agent will always ask to review in strict mode.", "在严格模式下，智能体将始终请求审核。")
        .replaceAll("智能体 cannot modify files outside of the workspace in strict mode.", "在严格模式下，智能体无法修改工作区之外的文件。")
        .replaceAll("Agent cannot modify files outside of the workspace in strict mode.", "在严格模式下，智能体无法修改工作区之外的文件。")
        .replaceAll('"始终继续" is enabled without sandbox protection. This is very dangerous and we do not recommend doing this.', '"始终继续" 在没有沙盒保护的情况下被启用。这非常危险，我们不建议这样做。')
        .replaceAll("You currently don't have any MCP 服务器 installed. Add an MCP server above or add a custom one via the MCP Config.", "你目前没有安装任何 MCP 服务器。请在上方添加 MCP 服务器，或通过 MCP 配置添加自定义服务器。")
        .replaceAll("You currently don't have any MCP servers installed. Add an MCP server above or add a custom one via the MCP Config.", "你目前没有安装任何 MCP 服务器。请在上方添加 MCP 服务器，或通过 MCP 配置添加自定义服务器。")
        .replaceAll("插件 are packaged collections of skills and MCPs to help the 智能体 in Antigravity IDE work with Google developer products. You can always change your choices in 设置.", "插件是将技能和 MCP 打包的集合，用于帮助 Antigravity IDE 中的智能体更好地工作。你随时可以在“设置”中更改你的选择。")
        .replaceAll("Extensions are packaged collections of skills and MCPs to help the agent in Antigravity IDE work with Google developer products. You can always change your choices in Settings.", "插件是将技能和 MCP 打包的集合，用于帮助 Antigravity IDE 中的智能体更好地工作。你随时可以在“设置”中更改你的选择。")
        .replaceAll("Build With Google 插件", "Google 开发插件")
        .replaceAll("Build With Google Extensions", "Google 开发插件")
        .replaceAll("Build with Antigravity IDE 插件", "Antigravity IDE 官方插件")
        .replaceAll("Build with Antigravity IDE Extensions", "Antigravity IDE 官方插件")
        .replaceAll("Core tools and knowledge required to develop for Android", "开发 Android 所需的核心工具和知识")
        .replaceAll("Keep your coding agent up to date with the latest web best practices.", "让你的编程智能体掌握最新的 Web 最佳实践。")
        .replaceAll("Using the Antigravity Python SDK to build AI agents", "使用 Antigravity Python SDK 构建 AI 智能体")
        .replaceAll("Curated collection of agent skills for science.", "为科学研究精选的智能体技能集合。")
        .replaceAll("Prototype, build & run modern apps users love with Firebase's backend, AI, and operational infrastructure.", "使用 Firebase 的后端、AI 和运维基础设施，制作原型、构建并运行广受用户喜爱的现代应用。")
        .replaceAll("Reliable automation, in-depth debugging, and performance analysis in Chrome using Chrome DevTools and Puppeteer", "使用 Chrome DevTools 和 Puppeteer 在 Chrome 中实现可靠的自动化、深入调试和性能分析")
        .replaceAll("Ask anything, @ to mention, / for actions", "有事请问，使用 @ 提及对象，使用 / 唤出操作")
        .replaceAll("打开 智能体 on 重载", "重载时打开智能体面板")
        .replaceAll("Open Agent on reload", "重载时打开智能体面板")
        .replaceAll("智能体's", "智能体的")
        .replaceAll("智能体 settings", "智能体设置")
        .replaceAll("智能体 panel", "智能体面板")
        .replaceAll("终端 commands", "终端命令")
        .replaceAll("MCP 工具s", "MCP 工具")
        .replaceAll("URL s", "URL")
        .replaceAll("URLs", "URL");
    if (houChuLi !== zhuTi) jieGuo = houChuLi;
    if (jieGuo === zhuTi) jieGuo = '';
    return jieGuo ? qian + jieGuo + hou : yuanWen;
  }}

  function keFanYiYuanSu(yuanSu) {{
    if (!yuanSu) return false;
    if (tiaoGuoBiaoQian.has(yuanSu.tagName)) {{
        const text = yuanSu.textContent || "";
        if (/Select\\W+one\\W+of\\W+the\\W+three\\W+options/i.test(text)) {{
            return !yuanSu.closest(tiaoGuoXuanZeQi);
        }}
        return false;
    }}
    return !yuanSu.closest(tiaoGuoXuanZeQi);
  }}

  function fanYiYuanSuShuXing(yuanSu) {{
    for (const ming of ['title', 'aria-label', 'placeholder']) {{
      const zhi = yuanSu.getAttribute && yuanSu.getAttribute(ming);
      if (zhi) {{
        const xinZhi = fanYiWenBen(zhi);
        if (xinZhi !== zhi) yuanSu.setAttribute(ming, xinZhi);
      }}
    }}
  }}

  function fanYiJieDian(gen) {{
    if (!gen) return;
    if (gen.nodeType === Node.TEXT_NODE) {{
      const fu = gen.parentElement;
      if (!keFanYiYuanSu(fu)) return;
      const xinZhi = fanYiWenBen(gen.nodeValue);
      if (xinZhi !== gen.nodeValue) gen.nodeValue = xinZhi;
      return;
    }}
    if (gen.nodeType !== Node.ELEMENT_NODE || !keFanYiYuanSu(gen)) return;
    fanYiYuanSuShuXing(gen);
    const shu = document.createTreeWalker(gen, NodeFilter.SHOW_TEXT, {{
      acceptNode(jieDian) {{
        return keFanYiYuanSu(jieDian.parentElement) ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT;
      }}
    }});
    const daiChuLi = [];
    while (shu.nextNode()) daiChuLi.push(shu.currentNode);
    for (const jieDian of daiChuLi) {{
      const xinZhi = fanYiWenBen(jieDian.nodeValue);
      if (xinZhi !== jieDian.nodeValue) jieDian.nodeValue = xinZhi;
    }}
    for (const yuanSu of gen.querySelectorAll('[title], [aria-label], [placeholder]')) {{
      if (keFanYiYuanSu(yuanSu)) fanYiYuanSuShuXing(yuanSu);
    }}
    for (const yuanSu of gen.querySelectorAll('*')) {{
      if (yuanSu.shadowRoot) fanYiJieDian(yuanSu.shadowRoot);
    }}
  }}

  let paiDui = false;
  function anPaiFanYi() {{
    if (paiDui) return;
    paiDui = true;
    requestAnimationFrame(() => {{
      paiDui = false;
      fanYiJieDian(document.body);
    }});
  }}

  window.addEventListener('DOMContentLoaded', anPaiFanYi);
  new MutationObserver(anPaiFanYi).observe(document.documentElement, {{
    childList: true,
    subtree: true,
    characterData: true,
    attributes: true,
    attributeFilter: ['title', 'aria-label', 'placeholder']
  }});
  anPaiFanYi();
  let chongSaoCiShu = 0;
  const chongSaoJiShiQi = setInterval(() => {{
    chongSaoCiShu += 1;
    anPaiFanYi();
    if (chongSaoCiShu >= 30) clearInterval(chongSaoJiShiQi);
  }}, 1000);
}})();
"""


def 注入脚本(html内容: str) -> str:
    if 注入标记 in html内容:
        return html内容
    标签 = f'<!-- {注入标记} -->\n<script src="./{脚本文件名}" type="module"></script>\n'
    候选目标 = [
        '<script src="./workbench.js" type="module"></script>',
        '<script src="./jetskiAgent.js" type="module"></script>',
    ]
    for 目标 in 候选目标:
        if 目标 in html内容:
            return html内容.replace(目标, 标签 + 目标, 1)
    raise RuntimeError("未找到可识别的启动脚本标签，无法安全注入。")


def 更新产品校验(product路径: Path, 文件: dict[str, Path]) -> None:
    数据 = json.loads(读取文本(product路径))
    checksums = 数据.setdefault("checksums", {})
    for 键, 校验键 in HTML校验路径.items():
        checksums[校验键] = 计算校验值(文件[键])
    写入文本(product路径, json.dumps(数据, ensure_ascii=False, indent="\t") + "\n")


def 安装(安装目录: Path) -> None:
    文件 = 定位文件(安装目录)
    for 键 in HTML校验路径:
        备份一次(文件[键])
    备份一次(文件["product"])

    写入文本(文件["js"], 生成汉化脚本())
    for 键 in HTML校验路径:
        新内容 = 注入脚本(读取文本(文件[键]))
        写入文本(文件[键], 新内容)
    更新产品校验(文件["product"], 文件)
    print("[完成] 已安装 Antigravity IDE 汉化补丁。请完全退出并重启 Antigravity IDE。")


def 恢复(安装目录: Path) -> None:
    文件 = 定位文件(安装目录)
    for 键 in [*HTML校验路径.keys(), "product"]:
        备份路径 = 文件[键].with_name(文件[键].name + 备份后缀)
        if not 备份路径.exists():
            raise FileNotFoundError(f"未找到备份文件：{备份路径}")
        shutil.copy2(备份路径, 文件[键])
    if 文件["js"].exists():
        文件["js"].unlink()
    print("[完成] 已恢复 Antigravity IDE 原始文件。请重启 Antigravity IDE。")


def 状态(安装目录: Path) -> None:
    文件 = 定位文件(安装目录)
    workbench内容 = 读取文本(文件["workbench"])
    jetski内容 = 读取文本(文件["jetski"])
    product数据 = json.loads(读取文本(文件["product"]))
    print(f"安装目录：{安装目录}")
    print(f"IDE 版本：{product数据.get('ideVersion', '未知')}")
    print(f"VS Code 基线版本：{product数据.get('version', '未知')}")
    print(f"workbench 汉化注入：{'是' if 注入标记 in workbench内容 else '否'}")
    print(f"jetski 设置页汉化注入：{'是' if 注入标记 in jetski内容 else '否'}")
    print(f"汉化脚本：{'存在' if 文件['js'].exists() else '不存在'}")
    for 键, 校验键 in HTML校验路径.items():
        当前校验 = 计算校验值(文件[键])
        记录校验 = product数据.get("checksums", {}).get(校验键)
        print(f"{键} 校验匹配：{'是' if 当前校验 == 记录校验 else '否'}")
        print(f"{键} 备份：{'存在' if 文件[键].with_name(文件[键].name + 备份后缀).exists() else '不存在'}")
    print(f"product 备份：{'存在' if 文件['product'].with_name(文件['product'].name + 备份后缀).exists() else '不存在'}")


def main() -> int:
    解析器 = argparse.ArgumentParser(description="Antigravity IDE 汉化补丁工具")
    解析器.add_argument("命令", choices=["status", "install", "restore"], help="要执行的操作")
    解析器.add_argument("--install-dir", default=str(默认安装目录), help="Antigravity IDE 安装目录")
    参数 = 解析器.parse_args()

    安装目录 = Path(参数.install_dir)
    try:
        if 参数.命令 == "status":
            状态(安装目录)
        elif 参数.命令 == "install":
            安装(安装目录)
        elif 参数.命令 == "restore":
            恢复(安装目录)
    except Exception as 错误:
        print(f"[错误] {错误}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
