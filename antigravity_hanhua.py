# -*- coding: utf-8 -*-
"""Antigravity 外壳汉化补丁工具。

用法：
  python antigravity_hanhua.py status
  python antigravity_hanhua.py install
  python antigravity_hanhua.py restore
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


if sys.platform == "darwin":
    默认安装目录 = Path("/Applications/Antigravity.app/Contents")
else:
    默认安装目录 = Path(r"C:\Users\hongl\AppData\Local\Programs\Antigravity")
备份后缀 = ".agzh.bak"
注入标记 = "ANTIGRAVITY_HUB_ZH_CN_INJECTION"
ASAR_UNPACK目录表达式 = "node_modules/chrome-devtools-mcp"


def 定位文件(安装目录: Path) -> dict[str, Path]:
    resources目录 = 安装目录 / ("Resources" if sys.platform == "darwin" else "resources")
    文件 = {
        "asar": resources目录 / "app.asar",
        "asar_unpacked": resources目录 / "app.asar.unpacked",
        "bin": resources目录 / "bin",
    }
    缺失 = [str(路径) for 路径 in [文件["asar"], 文件["asar_unpacked"], 文件["bin"]] if not 路径.exists()]
    if 缺失:
        raise FileNotFoundError("缺少必要文件或目录：\n" + "\n".join(缺失))
    return 文件


def 运行_asar(参数: list[str]) -> None:
    npx命令 = shutil.which("npx.cmd") or shutil.which("npx")
    if not npx命令:
        raise RuntimeError("未找到 npx，无法调用 asar 工具。请先安装 Node.js。")
    命令 = [npx命令, "--yes", "asar", *参数]
    结果 = subprocess.run(命令, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if 结果.returncode != 0:
        输出 = (结果.stderr or 结果.stdout or "").strip()
        raise RuntimeError(f"asar 命令执行失败：{输出}")


def 备份一次(文件路径: Path) -> Path:
    备份路径 = 文件路径.with_name(文件路径.name + 备份后缀)
    if not 备份路径.exists():
        shutil.copy2(文件路径, 备份路径)
    return 备份路径


def 读取文本(文件路径: Path) -> str:
    return 文件路径.read_text(encoding="utf-8")


def 写入文本(文件路径: Path, 内容: str) -> None:
    文件路径.write_text(内容, encoding="utf-8", newline="")


def 生成页面汉化代码() -> str:
    词典 = {
        "File": "文件",
        "Edit": "编辑",
        "Selection": "选择",
        "View": "视图",
        "Go": "转到",
        "Run": "运行",
        "Terminal": "终端",
        "Window": "窗口",
        "Help": "帮助",
        "Minimize": "最小化",
        "Maximize": "最大化",
        "Close": "关闭",
        "Settings": "设置",
        "Copy": "复制",
        "Open": "打开",
        "Refresh": "刷新",
        "Submit": "提交",
        "Customize": "自定义",
        "Learn more": "了解更多",
        "Recommended": "推荐",
        "Global": "全局",
        "Plan": "套餐",
        "Description": "描述",
        "Setup": "设置",
        "Dark": "深色",
        "Light": "浅色",
        "System": "跟随系统",
        "Accent": "强调色",
        "Background": "背景",
        "Foreground": "前景",
        "Preset": "预设",
        "New Conversation": "新建对话",
        "Conversation History": "对话历史",
        "Scheduled Tasks": "计划任务",
        "Projects": "项目",
        "No conversations yet": "暂无对话",
        "Open IDE": "打开 IDE",
        "Ask anything, @ to mention, / for actions": "输入问题，@ 提及内容，/ 执行动作",
        "See all": "查看全部",
        "Focus Input": "聚焦输入框",
        "Open Conversation Picker": "打开对话选择器",
        "Open Settings": "打开设置",
        "Open System Preferences": "打开系统首选项",
        "Open Editor Settings": "打开编辑器设置",
        "Open File Search": "打开文件搜索",
        "Create Project": "创建项目",
        "Command Palette": "命令面板",
        "Select Next Conversation": "选择下一个对话",
        "Select Previous Conversation": "选择上一个对话",
        "Find in Pane": "在面板中查找",
        "Toggle Sidebar": "切换侧边栏",
        "Toggle Auxiliary Pane": "切换辅助面板",
        "Toggle Model Selector": "切换模型选择器",
        "Toggle Voice Recording": "切换语音录制",
        "Reset Zoom": "重置缩放",
        "Zoom In": "放大",
        "Zoom Out": "缩小",
        "Go Back": "后退",
        "Go Forward": "前进",
        "Message input": "消息输入框",
        "Send message": "发送消息",
        "Record voice memo": "录制语音备忘",
        "Add context": "添加上下文",
        "Good response": "好回复",
        "Bad response": "差回复",
        "Agent response": "智能体回复",
        "User message": "用户消息",
        "Display Options": "显示选项",
        "Sidebar": "侧边栏",
        "Typeahead menu": "联想菜单",
        "Undo changes up to this point": "撤销到此处之前的更改",
        "General": "通用",
        "Account": "账户",
        "Permissions": "权限",
        "Appearance": "外观",
        "Models": "模型",
        "Customizations": "自定义",
        "Browser": "浏览器",
        "App": "应用",
        "Show all": "显示全部",
        "Not in Project": "不在项目中",
        "Conversations": "对话",
        "Shortcuts": "快捷键",
        "Rules": "规则",
        "Token Usage": "Token 用量",
        "Project-Specific Settings": "项目专属设置",
        "Modify scoped permissions, folders, and agent settings like Sandbox and Terminal Command Execution.": "修改当前范围的权限、文件夹，以及沙盒和终端命令执行等智能体设置。",
        "Go To Projects": "转到项目",
        "File Permissions": "文件权限",
        "Keyboard shortcuts for quick navigation and control.": "用于快速导航和控制的键盘快捷键。",
        "Manage project folders, agent settings, and permissions.": "管理项目文件夹、智能体设置和权限。",
        "Folders": "文件夹",
        "Add Folder": "添加文件夹",
        "Agent Settings": "智能体设置",
        "Security Preset": "安全预设",
        "Choose a predefined security preset for the agent. This controls terminal auto-execution policy, and file access policy.": "为智能体选择预设安全策略。该策略会控制终端自动执行策略和文件访问策略。",
        "Learn more about": "了解更多",
        "Turbo mode": "极速模式",
        "Default": "默认",
        "Full machine": "整机访问",
        "Custom": "自定义",
        "Requires manual review for all terminal commands and file accesses outside of the working folders.": "工作文件夹之外的所有终端命令和文件访问都需要人工审核。",
        "All terminal commands require review. The agent can read or write to any file in the machine.": "所有终端命令都需要审核。智能体可以读取或写入本机任意文件。",
        "Disables all safety barriers for maximal iteration velocity.": "禁用所有安全限制，以获得最快迭代速度。",
        "Agent Behavior": "智能体行为",
        "Artifact Review Policy": "产物审核策略",
        "Specifies Agent's behavior when asking for review on artifacts, which are documents it creates to enable a richer conversation experience.": "指定智能体在请求审核产物时的行为。产物是它为提供更丰富对话体验而创建的文档。",
        "Always Ask": "始终询问",
        "Always Proceed": "始终继续",
        "Request Approval": "请求审核",
        "Proceed in Sandbox": "在沙盒中继续",
        "Local Permissions": "本地权限",
        "Inherits from": "继承自",
        "global settings": "全局设置",
        "Local permissions have higher priority.": "本地权限优先级更高。",
        "The breakdown below shows token usage from customizations like skills, rules, and MCP. If the budget is exceeded, large customizations will be truncated automatically.": "下方显示技能、规则和 MCP 等自定义内容的 Token 用量明细。如果超出预算，大型自定义内容会被自动截断。",
        "% of the customization budget is available.": "的自定义预算可用。",
        "Show 1 breakdown": "显示 1 项明细",
        "Show 2 breakdowns": "显示 2 项明细",
        "Rules: 1,696 tokens": "规则：1,696 个 Token",
        "Manage your plan, credentials, and general preferences.": "管理你的套餐、凭据和通用偏好设置。",
        "Enable Telemetry": "启用遥测",
        "When toggled on, Antigravity collects usage data to help Google enhance performance and features.": "开启后，Antigravity 会收集使用数据，帮助 Google 提升性能和功能。",
        "Marketing Emails": "营销邮件",
        "Receive product updates, tips, and promotions from Google Antigravity via email.": "通过电子邮件接收 Google Antigravity 的产品更新、技巧和促销信息。",
        "Your Plan: Google AI Pro": "你的套餐：Google AI Pro",
        "You can upgrade to a Google AI Ultra plan to receive higher rate limits.": "你可以升级到 Google AI Ultra 套餐，以获得更高的速率限制。",
        "Email": "邮箱",
        "Upgrade": "升级",
        "Sign Out": "退出登录",
        "Terms of Service": "服务条款",
        "By using this app, you agree to its Terms of Service": "使用此应用即表示你同意其服务条款",
        "By using this app, you agree to its": "使用此应用即表示你同意其",
        "Your Plan:": "你的套餐：",
        "Model Credits": "模型额度",
        "Model Quota": "模型配额",
        "Gemini Models": "Gemini 模型",
        "Claude and GPT Models": "Claude 和 GPT 模型",
        "Enable AI Credit Overages": "启用 AI Credit 超额使用",
        "When toggled on, Antigravity will use your AI credits to fulfill model requests once you're out of model quota. Antigravity will always use your model quota first before using AI credits.": "开启后，当模型配额用完时，Antigravity 会使用你的 AI credits 来完成模型请求。Antigravity 会始终优先使用模型配额，然后才使用 AI credits。",
        "Within each group, models share a weekly limit and a 5-hour limit. Quota is consumed proportionally to the cost of the tokens. Thus, limits will last longer with shorter tasks or using more cost-effective models. The 5-hour limit smooths out aggregate demand to fairly distribute global capacity across all users, while your weekly limit is tied directly to your individual tier.": "每组模型共享每周限制和 5 小时限制。配额会按 Token 成本比例消耗。因此，任务越短或使用成本更低的模型，额度可持续越久。5 小时限制用于平滑整体需求，公平分配全球容量；每周限制则与你的个人套餐等级直接相关。",
        "Five Hour Limit": "五小时限制",
        "Weekly Limit": "每周限制",
        "You have used some of your 5-hour limit, it will fully refresh in 4 hours, 54 minutes.": "你已使用部分 5 小时额度，将在 4 小时 54 分钟后完全刷新。",
        "You have used some of your weekly limit, it will fully refresh in 2 days, 15 hours.": "你已使用部分每周额度，将在 2 天 15 小时后完全刷新。",
        "You have used some of your weekly limit, it will fully refresh in 3 days, 15 hours.": "你已使用部分每周额度，将在 3 天 15 小时后完全刷新。",
        "Refresh quota and credits data": "刷新配额和 credits 数据",
        "Agent security mode": "智能体安全模式",
        "Select one of the three options. Agent settings and permissions can be further customized below.": "请选择三种模式之一。智能体设置和权限可在下方继续自定义。",
        "Full access": "完全访问",
        "Sandboxed": "沙盒模式",
        "Strict": "严格模式",
        "Browser Settings": "浏览器设置",
        "Configure the browser subagent. It requires Google Chrome to be installed.": "配置浏览器子智能体。需要安装 Google Chrome。",
        "Enable Browser Tools": "启用浏览器工具",
        "Configure AI models and view your quota.": "配置 AI 模型并查看你的额度。",
        "Configure default behaviors, skills, and MCP servers.": "配置默认行为、技能和 MCP 服务器。",
        "Notification Settings": "通知设置",
        "Manage your notification preferences.": "管理你的通知偏好设置。",
        "To modify notification settings, open your operating system's system preferences.": "要修改通知设置，请打开操作系统的系统首选项。",
        "Notifications": "通知",
        "App Settings": "应用设置",
        "Manage application settings.": "管理应用设置。",
        "Prevent Sleep": "防止睡眠",
        "Prevent the computer from sleeping while the app is running.": "应用运行时防止电脑进入睡眠。",
        "Keep In Menu Bar": "保留在菜单栏",
        "The app will be accessible from the menu bar and will keep running in the background when all windows are closed.": "应用可从菜单栏访问，并会在所有窗口关闭后继续在后台运行。",
        "Chat Settings": "聊天设置",
        "Verbose agent chat": "详细智能体聊天",
        "Display and preserve intermediate thinking steps": "显示并保留中间思考步骤",
        "Layout Controls": "布局控制",
        "Select light, dark, or inherit system settings.": "选择浅色、深色或继承系统设置。",
        "Dark Theme": "深色主题",
        "Light Theme": "浅色主题",
        "Default Dark": "默认深色",
        "Default Light": "默认浅色",
        "One Light": "One 浅色",
        "Solarized Light": "Solarized 浅色",
        "File Access Rules": "文件访问规则",
        "Network Access Rules": "网络访问规则",
        "Terminal Commands": "终端命令",
        "Terminal & Tooling Permissions": "终端和工具权限",
        "Network Permissions": "网络权限",
        "Actuation Permissions": "执行权限",
        "Selection Actions": "选择操作",
        "Show Selection Actions": "显示选择操作",
        "Show \"Edit\" and \"Chat\" buttons when selecting text in the editor.": "在编辑器中选择文本时显示“编辑”和“聊天”按钮。",
        "To modify editor settings, open Settings within the editor window.": "要修改编辑器设置，请在编辑器窗口中打开设置。",
        "Open Editor Settings": "打开编辑器设置",
        "Navigation": "导航",
        "File Picker": "文件选择器",
        "Configure editor-specific behaviors and shortcuts.": "配置编辑器专属行为和快捷键。",
        "Marketplace": "市场",
        "Marketplace Item URL": "市场项目 URL",
        "Marketplace Gallery URL": "市场 Gallery URL",
        "Changes the base URL on each extension page. You must restart Antigravity to use the new marketplace after changing this value.": "更改每个扩展页面上的基础 URL。更改后必须重启 Antigravity 才能使用新的市场。",
        "Changes the base URL for marketplace search results. You must restart Antigravity to use the new marketplace after changing this value.": "更改市场搜索结果的基础 URL。更改后必须重启 Antigravity 才能使用新的市场。",
        "MCP Tools": "MCP 工具",
        "Installed MCP Servers": "已安装的 MCP 服务器",
        "No MCP Servers": "没有 MCP 服务器",
        "You currently don't have any MCP Servers installed.": "你当前没有安装任何 MCP 服务器。",
        "Add an MCP server above": "在上方添加 MCP 服务器",
        "Add MCP": "添加 MCP",
        "Build With Google Plugins": "Google 构建插件",
        "Configure external tools via Model Context Protocol.": "通过 Model Context Protocol 配置外部工具。",
        "Configure global allowed and denied resource permissions.": "配置全局允许和拒绝的资源权限。",
        "Configure allowed and denied paths for file reads and writes.": "配置文件读写允许和拒绝的路径。",
        "Configure allowed and denied URLs for reading.": "配置读取 URL 的允许和拒绝规则。",
        "Configure allowed and denied URLs for browser actuation.": "配置浏览器执行操作的 URL 允许和拒绝规则。",
        "Configure allowed terminal commands.": "配置允许的终端命令。",
        "Configure allowed commands outside the sandbox.": "配置允许在沙盒外运行的命令。",
        "Commands Outside Sandbox": "沙盒外命令",
        "Browser Actuation Rules": "浏览器执行规则",
        "Browser Javascript Execution Policy": "浏览器 JavaScript 执行策略",
        "Controls whether the agent can run custom JavaScript to automate complex browser actions.": "控制智能体是否可以运行自定义 JavaScript 来自动化复杂浏览器操作。",
        "Controls whether the agent can run custom Javascript to automate complex browser actions.": "控制智能体是否可以运行自定义 JavaScript 来自动化复杂浏览器操作。",
        "Disabled": "已禁用",
        "Block all browser JavaScript execution.": "阻止所有浏览器 JavaScript 执行。",
        "Prompt for approval before running browser scripts.": "运行浏览器脚本前请求批准。",
        "Allow full browser script execution without prompting.": "无需提示即可完整执行浏览器脚本。",
        "Terminal Command Auto Execution": "终端命令自动执行",
        "Controls whether terminal commands require your approval before running.": "控制终端命令在运行前是否需要你的批准。",
        "The agent never asks for confirmation before executing terminal commands (except those in the 拒绝 list). This provides the agent with the maximum ability to operate over long periods without intervention, but also has the highest risk of an agent executing an unsafe terminal command.": "智能体在执行终端命令前不会请求确认（拒绝列表中的命令除外）。这能让智能体长时间自主运行，但也带来执行不安全终端命令的最高风险。",
        "The command automatically proceeds if the command runs inside the sandbox. Otherwise, it requests review.": "如果命令在沙盒内运行，则自动继续；否则请求审核。",
        "The agent always asks for confirmation before executing terminal commands (except those in the 允许 list).": "智能体在执行终端命令前始终请求确认（允许列表中的命令除外）。",
        "Configure the agent's visual theme and display preferences.": "配置智能体的视觉主题和显示偏好。",
        "Configure tab completion, suggestions, and navigation behavior.": "配置 Tab 补全、建议和导航行为。",
        "The browser subagent can be invoked by typing /browser in the conversation input box.": "可在对话输入框中输入 /browser 来调用浏览器子智能体。",
        "Configure the browser subagent. It requires": "配置浏览器子智能体。需要安装",
        "to be installed.": "。",
        "Google Drive integration not available": "Google Drive 集成不可用",
        "Claude and GPT models": "Claude 和 GPT 模型",
        "Gemini models": "Gemini 模型",
        "Request Review": "请求审核",
        "Common Feedback": "通用反馈",
        "Provide Feedback": "提供反馈",
        "Send feedback as": "发送反馈，账号：",
        "Feedback Type": "反馈类型",
        "Bug Report": "错误报告",
        "Feature Request": "功能请求",
        "Actual behavior": "实际行为",
        "Expected behavior": "预期行为",
        "Steps to Reproduce": "复现步骤",
        "Steps to reproduce the issue": "复现问题的步骤",
        "Please list the steps to reproduce the issue": "请列出复现问题的步骤",
        "Attach a screenshot (optional)": "附加截图（可选）",
        "Attach Antigravity server logs": "附加 Antigravity 服务日志",
        "We recommend attaching logs. Attaching logs will help the Antigravity team act on and prioritize your feedback.": "建议附加日志。日志能帮助 Antigravity 团队处理并优先排序你的反馈。",
        "Any error messages": "任何错误信息",
        "Any relevant information": "任何相关信息",
        "Please describe the issue in detail. The more actionable your feedback, the quicker our team can address your request. Some helpful information includes:": "请详细描述问题。反馈越具体可执行，团队就越快处理。建议包含以下信息：",
        "Describe the bug you encountered...": "描述你遇到的错误...",
        "Auth and Billing": "认证和账单",
        "Conversation": "对话",
        "For help, visit": "如需帮助，请访问",
        "or join the": "或加入",
        "Jetski Chat": "Jetski Chat",
        "Setup Jetski Chat": "设置 Jetski Chat",
        "Configure a chat bot so you can use Jetski directly from Google Chat.": "配置聊天机器人，以便直接从 Google Chat 使用 Jetski。",
        "Bot Name": "机器人名称",
        "Avatar URL": "头像 URL",
        "Enter bot name (optional)": "输入机器人名称（可选）",
        "Enter avatar URL (optional)": "输入头像 URL（可选）",
        "Danger Zone": "危险区域",
        "Delete Project": "删除项目",
        "Permanently delete": "永久删除",
        "including": "包括",
        "and": "以及",
    }
    模式 = [
        [r"^Your Plan:\s*(.+)$", r"你的套餐：$1"],
        [r"^(\d+)\s+agents?\s+running$", r"$1 个智能体运行中"],
        [r"^No agents?\s+running$", r"没有智能体运行"],
        [r"^See all \((\d+)\)$", r"查看全部（$1）"],
        [r"^Worked for (\d+)m$", r"已工作 $1 分钟"],
        [r"^(\d+)d$", r"$1 天前"],
        [r"^(\d+)mo$", r"$1 个月前"],
        [r"^(\d+)m$", r"$1 分钟前"],
        [r"^Select model, current: (.+)$", r"选择模型，当前：$1"],
        [r"^(\d+)\s+active conversations?$", r"$1 个活跃对话"],
        [r"^(\d+)\s+archived conversations?$", r"$1 个归档对话"],
        [r"^Rules:\s*([\d,]+)\s+tokens$", r"规则：$1 个 Token"],
        [r"^Send feedback as (.+)$", r"发送反馈，账号：$1"],
        [r"^You have used some of your 5-hour limit, it will fully refresh in (\d+) hours?, (\d+) minutes?\.?$", r"你已使用部分 5 小时额度，将在 $1 小时 $2 分钟后完全刷新。"],
        [r"^You have used some of your weekly limit, it will fully refresh in (\d+) days?, (\d+) hours?\.?$", r"你已使用部分每周额度，将在 $1 天 $2 小时后完全刷新。"],
    ]
    模板 = r"""
(() => {
  if (window.__ANTIGRAVITY_PAGE_ZH_CN__) return;
  window.__ANTIGRAVITY_PAGE_ZH_CN__ = true;
  const ciDian = new Map(__CIDIAN__);
  const moShi = __MOSHI__.map(([yuan, xin]) => [new RegExp(yuan, 'i'), xin]);
  const tiaoGuoBiaoQian = new Set(['SCRIPT', 'STYLE', 'TEXTAREA', 'INPUT', 'CODE', 'PRE']);
  const tiaoGuoXuanZeQi = '.monaco-editor, .xterm, [contenteditable="true"]';

  function tiHuanDuanYu(wenBen, yuan, xin) {
    return wenBen.split(yuan).join(xin);
  }

  function fanYi(text) {{
    if (!text) return text;
    const qian = text.slice(0, text.length - text.trimStart().length);
    const hou = text.slice(text.trimEnd().length);
    const zhuTi = text.trim();
    if (!zhuTi) return text;
    let jieGuo = ciDian.get(zhuTi);
    if (!jieGuo) {{
      for (const [re, tiHuan] of moShi) {{
        if (re.test(zhuTi)) {{
          jieGuo = zhuTi.replace(re, tiHuan);
          break;
        }}
      }}
    }}
    if (!jieGuo) {{
      jieGuo = zhuTi;
      for (const [yingWen, zhongWen] of Array.from(ciDian.entries()).sort((a, b) => b[0].length - a[0].length)) {{
        if (yingWen.length >= 10 && yingWen.includes(' ') && jieGuo.includes(yingWen)) jieGuo = tiHuanDuanYu(jieGuo, yingWen, zhongWen);
      }}
    }}
    jieGuo = jieGuo
      .replaceAll('编辑or', '编辑器')
      .replaceAll('编辑ing', 'Editing')
      .replaceAll('了解更多 about', '了解更多')
      .replaceAll('允许 list', '允许列表')
      .replaceAll('拒绝 list', '拒绝列表')
      .replaceAll('Local 权限', '本地权限')
      .replaceAll('终端 Command Execution', '终端命令执行')
      .replaceAll('编辑器 Settings', '编辑器设置')
      .replaceAll('文件 Picker', '文件选择器')
      .replaceAll('文件 Access Rules', '文件访问规则')
      .replaceAll('Network 权限', '网络权限')
      .replaceAll('Actuation 权限', '执行权限')
      .replaceAll('选择 Actions', '选择操作')
      .replaceAll('Show 选择操作', '显示选择操作')
      .replaceAll('终端 Commands', '终端命令')
      .replaceAll('终端 & Tooling 权限', '终端和工具权限')
      .replaceAll('浏览器 Actuation Rules', '浏览器执行规则')
      .replaceAll('浏览器 Javascript Execution Policy', '浏览器 JavaScript 执行策略')
      .replaceAll('通用 Feedback', '通用反馈')
      .replaceAll('Open 编辑器 Settings', '打开编辑器设置')
      .replaceAll('Open 文件 Search', '打开文件搜索')
      .replaceAll('Go to 项目', '转到项目')
      .replaceAll('Gemini 模型', 'Gemini 模型');
    if (jieGuo === zhuTi) return text;
    return qian + jieGuo + hou;
  }}

  function keFanYiYuanSu(yuanSu) {{
    if (!yuanSu || tiaoGuoBiaoQian.has(yuanSu.tagName)) return false;
    return !yuanSu.closest(tiaoGuoXuanZeQi) || !!yuanSu.closest('[role="dialog"], nav, aside, header, [data-testid]');
  }}

  function fanYiShuXing(yuanSu) {{
    for (const ming of ['title', 'aria-label', 'placeholder']) {{
      const zhi = yuanSu.getAttribute && yuanSu.getAttribute(ming);
      if (!zhi) continue;
      const xinZhi = fanYi(zhi);
      if (xinZhi !== zhi) yuanSu.setAttribute(ming, xinZhi);
    }}
  }

  function fanYiSuoYouShuXing(root) {{
    if (!root || !root.querySelectorAll) return;
    for (const yuanSu of root.querySelectorAll('[title], [aria-label], [placeholder]')) {{
      fanYiShuXing(yuanSu);
    }}
  }}

  function saoMiao(root) {{
    if (!root) return;
    if (root.nodeType === Node.ELEMENT_NODE && !keFanYiYuanSu(root)) return;
    const shu = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {{
      acceptNode(jieDian) {{
        return keFanYiYuanSu(jieDian.parentElement) ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT;
      }}
    }});
    const jieDian = [];
    while (shu.nextNode()) jieDian.push(shu.currentNode);
    for (const item of jieDian) {{
      const xinZhi = fanYi(item.nodeValue);
      if (xinZhi !== item.nodeValue) item.nodeValue = xinZhi;
    }}
    if (root.querySelectorAll) {{
      fanYiSuoYouShuXing(root);
      for (const yuanSu of root.querySelectorAll('*')) {{
        if (yuanSu.shadowRoot) saoMiao(yuanSu.shadowRoot);
      }}
    }}
  }}

  let paiDui = false;
  function anPai() {{
    if (paiDui) return;
    paiDui = true;
    requestAnimationFrame(() => {{
      paiDui = false;
      saoMiao(document.body || document.documentElement);
    }});
  }

  window.addEventListener('DOMContentLoaded', anPai);
  new MutationObserver(anPai).observe(document.documentElement, {{
    childList: true,
    subtree: true,
    characterData: true,
    attributes: true,
    attributeFilter: ['title', 'aria-label', 'placeholder']
  }});
  saoMiao(document.body || document.documentElement);
  anPai();
  let ciShu = 0;
  const timer = setInterval(() => {{
    ciShu += 1;
    anPai();
    if (ciShu >= 60) clearInterval(timer);
  }}, 1000);
})();
"""
    return (
        模板.replace("{{", "{")
        .replace("}}", "}")
        .replace("__CIDIAN__", json.dumps(list(词典.items()), ensure_ascii=False))
        .replace("__MOSHI__", json.dumps(模式, ensure_ascii=False))
    )


def 生成DOM汉化脚本() -> str:
    页面代码 = 生成页面汉化代码()
    页面代码JSON = json.dumps(页面代码, ensure_ascii=False)
    return f"""
// {注入标记}
;(() => {{
  if (globalThis.__ANTIGRAVITY_HUB_ZH_CN__) return;
  globalThis.__ANTIGRAVITY_HUB_ZH_CN__ = true;
  const zhuRu = () => {{
    try {{
      const daiMa = {页面代码JSON};
      electron_1.webFrame.executeJavaScript(daiMa, true).catch((cuoWu) => {{
        console.warn('[Antigravity 汉化] 主世界注入失败', cuoWu);
      }});
    }} catch (cuoWu) {{
      console.warn('[Antigravity 汉化] DOM 汉化脚本执行失败', cuoWu);
    }}
  }};
  if (document.readyState === 'loading') {{
    window.addEventListener('DOMContentLoaded', zhuRu, {{ once: true }});
  }} else {{
    zhuRu();
  }}
  setTimeout(zhuRu, 1000);
  setTimeout(zhuRu, 3000);
}})();
"""


def 替换文本(文件路径: Path, 替换表: list[tuple[str, str]]) -> int:
    内容 = 读取文本(文件路径)
    原内容 = 内容
    for 原文, 新文 in 替换表:
        内容 = 内容.replace(原文, 新文)
    if 内容 != 原内容:
        写入文本(文件路径, 内容)
    return 0 if 内容 == 原内容 else 1


def 补丁_wizard_html(解包目录: Path) -> int:
    文件路径 = 解包目录 / "dist" / "ideInstall" / "wizardHtml.js"
    return 替换文本(
        文件路径,
        [
            ("<html lang=\"en\">", "<html lang=\"zh-CN\">"),
            ("<title>Welcome to Antigravity</title>", "<title>欢迎使用 Antigravity</title>"),
            ("Welcome to the new Antigravity!", "欢迎使用新版 Antigravity！"),
            (
                "Antigravity has been redesigned to put agents first with new capabilities. If you'd still like a code editor, you can download it as a separate app named <b>Antigravity IDE</b>.",
                "Antigravity 已重新设计为以智能体为核心，并提供新的能力。如果你仍需要代码编辑器，可以下载名为 <b>Antigravity IDE</b> 的独立应用。",
            ),
            ("Download the Antigravity IDE", "下载 Antigravity IDE"),
            ("Explore the new Antigravity", "进入新版 Antigravity"),
        ],
    )


def 补丁_main(解包目录: Path) -> int:
    文件路径 = 解包目录 / "dist" / "main.js"
    return 替换文本(
        文件路径,
        [
            ("label: 'New Window'", "label: '新建窗口'"),
            ("label: 'No agents running'", "label: '没有智能体运行'"),
            ("label: `Open ${electron_1.app.getName()}`", "label: `打开 ${electron_1.app.getName()}`"),
            ("label: 'Quit'", "label: '退出'"),
            ("buttons: ['Cancel', 'Quit']", "buttons: ['取消', '退出']"),
            ("title: 'Confirm Quit'", "title: '确认退出'"),
            ("message: 'Are you sure you want to quit?'", "message: '确定要退出吗？'"),
            ("detail: 'There may be agents or background tasks running.'", "detail: '可能仍有智能体或后台任务正在运行。'"),
        ],
    )


def 补丁_menu(解包目录: Path) -> int:
    文件路径 = 解包目录 / "dist" / "menu.js"
    变更数 = 替换文本(
        文件路径,
        [
            ("label: 'New Window'", "label: '新建窗口'"),
            ("label: 'Docs'", "label: '文档'"),
        ],
    )
    内容 = 读取文本(文件路径)
    if "function translateMenuLabels" not in 内容:
        插入点 = "    // Re-apply the menu so the change takes effect.\n    electron_1.Menu.setApplicationMenu(menu);"
        新片段 = """    translateMenuLabels(menu);
    // Re-apply the menu so the change takes effect.
    electron_1.Menu.setApplicationMenu(menu);"""
        内容 = 内容.replace(插入点, 新片段, 1)
        内容 += """
function translateMenuLabels(menu) {
    const labelMap = {
        File: '文件',
        Edit: '编辑',
        Selection: '选择',
        View: '视图',
        Go: '转到',
        Run: '运行',
        Terminal: '终端',
        Window: '窗口',
        Help: '帮助',
        Undo: '撤销',
        Redo: '重做',
        Cut: '剪切',
        Copy: '复制',
        Paste: '粘贴',
        SelectAll: '全选',
        'New Window': '新建窗口',
        'New Conversation': '新建对话',
        'Create Project': '创建项目',
        'Command Palette': '命令面板',
        Docs: '文档',
    };
    const visit = (items) => {
        for (const item of items || []) {
            if (item.label && labelMap[item.label]) {
                item.label = labelMap[item.label];
            }
            if (item.submenu) {
                visit(item.submenu.items);
            }
        }
    };
    visit(menu.items);
}
"""
        写入文本(文件路径, 内容)
        变更数 += 1
    return 变更数


def 补丁_tray(解包目录: Path) -> int:
    文件路径 = 解包目录 / "dist" / "tray.js"
    原片段 = """countItem.label =
                (count > 0 ? `${count}` : 'No') +
                    ' agent' +
                    (count === 1 ? '' : 's') +
                    ' running';"""
    新片段 = """countItem.label = count > 0 ? `${count} 个智能体运行中` : '没有智能体运行';"""
    return 替换文本(文件路径, [(原片段, 新片段)])


def 补丁_updater(解包目录: Path) -> int:
    文件路径 = 解包目录 / "dist" / "updater.js"
    return 替换文本(
        文件路径,
        [
            ('MenuUpdateStep["CheckForUpdates"] = "Check for Updates";', 'MenuUpdateStep["CheckForUpdates"] = "检查更新";'),
            ('MenuUpdateStep["CheckingForUpdates"] = "Checking for Updates...";', 'MenuUpdateStep["CheckingForUpdates"] = "正在检查更新...";'),
            ('MenuUpdateStep["DownloadingUpdate"] = "Downloading Update...";', 'MenuUpdateStep["DownloadingUpdate"] = "正在下载更新...";'),
            ('MenuUpdateStep["RestartToUpdate"] = "Restart to Update";', 'MenuUpdateStep["RestartToUpdate"] = "重启以更新";'),
            ("title: 'Check for Updates'", "title: '检查更新'"),
            ("message: 'No updates available'", "message: '没有可用更新'"),
            ("buttons: ['OK']", "buttons: ['确定']"),
        ],
    )


def 补丁_ipc_handlers(解包目录: Path) -> int:
    文件路径 = 解包目录 / "dist" / "ipcHandlers.js"
    return 替换文本(文件路径, [("title: 'Open workspace'", "title: '打开工作区'")])


def 补丁_utils(解包目录: Path) -> int:
    文件路径 = 解包目录 / "dist" / "utils.js"
    内容 = 读取文本(文件路径)
    if 注入标记 in 内容:
        return 0
    页面代码JSON = json.dumps(生成页面汉化代码(), ensure_ascii=False)
    注入片段 = f"""
    // {注入标记}
    const antigravityZhCnCode = {页面代码JSON};
    const runAntigravityZhCnInPage = async (page) => {{
        const ws = new WebSocket(page.webSocketDebuggerUrl);
        let commandId = 0;
        const pending = new Map();
        ws.onmessage = (event) => {{
            const message = JSON.parse(event.data);
            if (message.id && pending.has(message.id)) {{
                pending.get(message.id)(message);
                pending.delete(message.id);
            }}
        }};
        await new Promise((resolve, reject) => {{
            ws.onopen = resolve;
            ws.onerror = reject;
            setTimeout(() => reject(new Error('WebSocket 连接超时')), 3000);
        }});
        const send = (method, params = {{}}) => new Promise((resolve) => {{
            const id = ++commandId;
            pending.set(id, resolve);
            ws.send(JSON.stringify({{ id, method, params }}));
        }});
        try {{
            await send('Runtime.enable');
            await send('Page.addScriptToEvaluateOnNewDocument', {{ source: antigravityZhCnCode }});
            await send('Runtime.evaluate', {{
                expression: antigravityZhCnCode,
                awaitPromise: true,
                returnByValue: true,
            }});
        }} finally {{
            ws.close();
        }}
    }};
    const runAntigravityZhCn = async () => {{
        try {{
            const portFile = path_1.default.join(electron_1.app.getPath('userData'), 'DevToolsActivePort');
            if (!fs.existsSync(portFile)) return;
            const port = fs.readFileSync(portFile, 'utf8').split(/\\r?\\n/)[0]?.trim();
            if (!port) return;
            const response = await fetch(`http://127.0.0.1:${{port}}/json/list`);
            const targets = await response.json();
            const pages = targets.filter((target) => target.type === 'page' && target.webSocketDebuggerUrl);
            for (const page of pages) {{
                await runAntigravityZhCnInPage(page);
            }}
        }} catch (error) {{
            console.warn('[Antigravity 汉化] 远程调试页面注入失败', error);
        }}
    }};
    win.webContents.on('dom-ready', runAntigravityZhCn);
    win.webContents.on('did-finish-load', runAntigravityZhCn);
    win.webContents.on('did-frame-finish-load', (_event, isMainFrame) => {{
        if (isMainFrame) {{
            runAntigravityZhCn();
        }}
    }});
    let antigravityZhCnRetryCount = 0;
    const antigravityZhCnRetryTimer = setInterval(() => {{
        antigravityZhCnRetryCount += 1;
        runAntigravityZhCn();
        if (antigravityZhCnRetryCount >= 60 || win.isDestroyed()) {{
            clearInterval(antigravityZhCnRetryTimer);
        }}
    }}, 1000);
"""
    目标 = "    void win.loadURL(url);\n    return win;"
    if 目标 not in 内容:
        raise RuntimeError("未找到 utils.js 中的窗口加载位置，无法安全注入主进程汉化脚本。")
    写入文本(文件路径, 内容.replace(目标, 注入片段 + "    void win.loadURL(url);\n    return win;", 1))
    return 1


def 补丁_preload(解包目录: Path) -> int:
    文件路径 = 解包目录 / "dist" / "preload.js"
    内容 = 读取文本(文件路径)
    if 注入标记 in 内容:
        return 0
    写入文本(文件路径, 内容.rstrip() + "\n" + 生成DOM汉化脚本())
    return 1


def 应用补丁(解包目录: Path) -> int:
    变更数 = 0
    for 操作 in [补丁_wizard_html, 补丁_main, 补丁_menu, 补丁_tray, 补丁_updater, 补丁_ipc_handlers, 补丁_utils, 补丁_preload]:
        变更数 += 操作(解包目录)
    return 变更数


def 解包到临时目录(asar路径: Path, unpacked目录: Path | None = None) -> Path:
    临时目录 = Path(tempfile.mkdtemp(prefix="antigravity_hanhua_"))
    if unpacked目录 is None:
        运行_asar(["extract", str(asar路径), str(临时目录)])
        return 临时目录

    # asar 对 unpacked 文件会按“asar 文件名 + .unpacked”寻找旁路目录。
    # 备份文件名是 app.asar.agzh.bak，因此需要临时复制成标准名称后再解包。
    临时源目录 = Path(tempfile.mkdtemp(prefix="antigravity_asar_source_"))
    try:
        临时asar = 临时源目录 / "app.asar"
        临时unpacked = 临时源目录 / "app.asar.unpacked"
        shutil.copy2(asar路径, 临时asar)
        if unpacked目录.exists():
            shutil.copytree(unpacked目录, 临时unpacked)
        运行_asar(["extract", str(临时asar), str(临时目录)])
    finally:
        shutil.rmtree(临时源目录, ignore_errors=True)
    return 临时目录


def 打包_asar(解包目录: Path, 输出路径: Path) -> None:
    if 输出路径.exists():
        输出路径.unlink()
    运行_asar(["pack", str(解包目录), str(输出路径), "--unpack-dir", ASAR_UNPACK目录表达式])


def 校验解包结构(解包目录: Path) -> dict:
    package路径 = 解包目录 / "package.json"
    preload路径 = 解包目录 / "dist" / "preload.js"
    wizard路径 = 解包目录 / "dist" / "ideInstall" / "wizardHtml.js"
    缺失 = [str(路径) for 路径 in [package路径, preload路径, wizard路径] if not 路径.exists()]
    if 缺失:
        raise FileNotFoundError("app.asar 结构不符合预期，缺少：\n" + "\n".join(缺失))
    return json.loads(读取文本(package路径))


def 安装(安装目录: Path) -> None:
    文件 = 定位文件(安装目录)
    备份路径 = 备份一次(文件["asar"])
    # 每次从原始备份重新生成补丁，避免旧版注入代码残留。
    临时目录 = 解包到临时目录(备份路径, 文件["asar_unpacked"])
    新asar = Path(tempfile.gettempdir()) / "antigravity_hanhua_app.asar"
    try:
        package数据 = 校验解包结构(临时目录)
        变更数 = 应用补丁(临时目录)
        打包_asar(临时目录, 新asar)
        shutil.copy2(新asar, 文件["asar"])
        print(f"[完成] 已安装 Antigravity 汉化补丁。版本：{package数据.get('version', '未知')}，变更模块数：{变更数}。")
        print("[提示] 请完全退出并重启 Antigravity。")
    finally:
        shutil.rmtree(临时目录, ignore_errors=True)
        if 新asar.exists():
            新asar.unlink()
        新unpacked = 新asar.with_name(新asar.name + ".unpacked")
        if 新unpacked.exists():
            shutil.rmtree(新unpacked, ignore_errors=True)


def 恢复(安装目录: Path) -> None:
    文件 = 定位文件(安装目录)
    备份路径 = 文件["asar"].with_name(文件["asar"].name + 备份后缀)
    if not 备份路径.exists():
        raise FileNotFoundError(f"未找到备份文件：{备份路径}")
    shutil.copy2(备份路径, 文件["asar"])
    print("[完成] 已恢复 Antigravity 原始 app.asar。请重启 Antigravity。")


def 状态(安装目录: Path) -> None:
    文件 = 定位文件(安装目录)
    临时目录 = 解包到临时目录(文件["asar"])
    try:
        package数据 = 校验解包结构(临时目录)
        preload内容 = 读取文本(临时目录 / "dist" / "preload.js")
        utils内容 = 读取文本(临时目录 / "dist" / "utils.js")
        wizard内容 = 读取文本(临时目录 / "dist" / "ideInstall" / "wizardHtml.js")
        print(f"安装目录：{安装目录}")
        print(f"应用版本：{package数据.get('version', '未知')}")
        print(f"app.asar：{文件['asar']}")
        print(f"app.asar 备份：{'存在' if 文件['asar'].with_name(文件['asar'].name + 备份后缀).exists() else '不存在'}")
        print(f"主进程页面汉化注入：{'是' if 注入标记 in utils内容 else '否'}")
        print(f"preload DOM 汉化注入：{'是' if 注入标记 in preload内容 else '否'}")
        print(f"安装向导静态汉化：{'是' if '欢迎使用新版 Antigravity' in wizard内容 else '否'}")
    finally:
        shutil.rmtree(临时目录, ignore_errors=True)


def 自检(安装目录: Path) -> None:
    文件 = 定位文件(安装目录)
    临时目录 = 解包到临时目录(文件["asar"])
    新asar = Path(tempfile.gettempdir()) / "antigravity_hanhua_check.asar"
    try:
        校验解包结构(临时目录)
        应用补丁(临时目录)
        subprocess.run([sys.executable, "-m", "py_compile", str(Path(__file__))], check=True)
        node命令 = shutil.which("node")
        if node命令:
            for 相对路径 in ["dist/preload.js", "dist/main.js", "dist/utils.js", "dist/ideInstall/wizardHtml.js"]:
                subprocess.run([node命令, "--check", str(临时目录 / 相对路径)], check=True)
        打包_asar(临时目录, 新asar)
        print("[完成] 自检通过：Python 语法、关键 JS 语法和 asar 重打包均正常。")
    finally:
        shutil.rmtree(临时目录, ignore_errors=True)
        if 新asar.exists():
            新asar.unlink()
        新unpacked = 新asar.with_name(新asar.name + ".unpacked")
        if 新unpacked.exists():
            shutil.rmtree(新unpacked, ignore_errors=True)


def 运行时注入() -> None:
    node命令 = shutil.which("node")
    if not node命令:
        raise RuntimeError("未找到 node，无法执行运行时汉化注入。")
    if sys.platform == "darwin":
        appdata目录 = Path.home() / "Library" / "Application Support" / "Antigravity"
    else:
        appdata目录 = Path.home() / "AppData" / "Roaming" / "Antigravity"
    端口文件 = appdata目录 / "DevToolsActivePort"
    if not 端口文件.exists():
        raise FileNotFoundError("未找到 DevToolsActivePort。请先启动 Antigravity，再执行 inject。")
    页面代码JSON = json.dumps("delete window.__ANTIGRAVITY_PAGE_ZH_CN__;\n" + 生成页面汉化代码(), ensure_ascii=False)
    node脚本 = f"""
(async () => {{
  const fs = require('fs');
  const portFile = {json.dumps(str(端口文件).replace(chr(92), "/"), ensure_ascii=False)};
  const code = {页面代码JSON};
  const port = fs.readFileSync(portFile, 'utf8').split(/\\r?\\n/)[0].trim();
  const targets = await (await fetch(`http://127.0.0.1:${{port}}/json/list`)).json();
  const pages = targets.filter(t => t.type === 'page' && t.webSocketDebuggerUrl);
  if (!pages.length) throw new Error('未找到 Antigravity 页面 target');
  for (const page of pages) {{
    const ws = new WebSocket(page.webSocketDebuggerUrl);
    let id = 0;
    const pending = new Map();
    ws.onmessage = event => {{
      const msg = JSON.parse(event.data);
      if (msg.id && pending.has(msg.id)) {{
        pending.get(msg.id)(msg);
        pending.delete(msg.id);
      }}
    }};
    await new Promise((resolve, reject) => {{ ws.onopen = resolve; ws.onerror = reject; }});
    const send = (method, params = {{}}) => new Promise(resolve => {{
      const callId = ++id;
      pending.set(callId, resolve);
      ws.send(JSON.stringify({{ id: callId, method, params }}));
    }});
    await send('Runtime.enable');
    const result = await send('Runtime.evaluate', {{
      expression: code,
      awaitPromise: true,
      returnByValue: true,
    }});
    if (result.error || (result.result && result.result.exceptionDetails)) {{
      console.error(JSON.stringify(result, null, 2));
      throw new Error(`页面注入失败: ${{page.url}}`);
    }}
    console.log(`[完成] 已运行时注入: ${{page.url}}`);
    ws.close();
  }}
}})().catch(error => {{
  console.error('[错误] ' + (error && error.message ? error.message : error));
  process.exit(1);
}});
"""
    subprocess.run([node命令, "-e", node脚本], check=True)


def main() -> int:
    解析器 = argparse.ArgumentParser(description="Antigravity 外壳汉化补丁工具")
    解析器.add_argument("命令", choices=["status", "install", "restore", "check", "inject"], help="要执行的操作")
    解析器.add_argument("--install-dir", default=str(默认安装目录), help="Antigravity 安装目录")
    参数 = 解析器.parse_args()

    安装目录 = Path(参数.install_dir)
    try:
        if 参数.命令 == "status":
            状态(安装目录)
        elif 参数.命令 == "install":
            安装(安装目录)
        elif 参数.命令 == "restore":
            恢复(安装目录)
        elif 参数.命令 == "check":
            自检(安装目录)
        elif 参数.命令 == "inject":
            运行时注入()
    except Exception as 错误:
        print(f"[错误] {错误}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
