# XiaoMate：一个真正干活的的开源桌宠“小美同学”

[TOC]

**你的桌面智能助理,构建你自己的数字分身,并让知识管理、任务提醒、自动化办公触手可及**

## 快速开始

### 通过 npm 安装(推荐)

```bash
# 全局安装
npm install -g xiaomate

# 运行方式一: 直接运行
npx xiaomate

# 运行方式二: 使用命令
xiaomate
```

**更新到最新版本:**
```bash
npm update -g xiaomate
```

**卸载:**
```bash
npm uninstall -g xiaomate
```

### 从源码运行

```bash
# 克隆仓库
git clone https://github.com/oddmeta/xiaomate-desktop.git
cd xiaomate-desktop

# 安装依赖
npm install

# 启动
npm start
```

---

趁这个国庆节，重新整理了一下 XiaoMate 的功能和界面，然后我又重整了一个 XiaoMate 的README 介绍。原先的技术太过于技术化了，许多人不懂技术的人看了一头雾水，这次改从 XiaoMate 所支持的功能出发，重写了一下。

- **愿景层** — 一个完全了解你的 AI，记得你经历过什么、思考过什么、面对过什么；困惑时像另一个你一样给建议，想分享经验时可以替你与他人对话
- **记录层** — 工作进展、学习心得、生活琐事、情绪波动，统统写进札记
- **AI 整理层** — 人物关系图谱、心情标签、情绪曲线
- **数字分身层** — 随着积累，XiaoMATE 越来越了解你；未来可以问"我曾经是怎么处理这类问题的？""我面对这种情况通常会怎么做？"，得到属于"你自己"的答案
- **情感层** — 既是安全的倾诉树洞，也是映照成长轨迹的镜子

后面有空的时候准备再写一个功能介绍的系列文章，将 XiaoMate 小美同学支持的每个功能都给一一介绍一下。等我有空了哈~~~

[![XiaoMate 小美同学](https://oddmeta.net/docs/xiaomate/resources/XiaoMATE.png)](http://oddmeta.net/docs/xiaomate/README.html)
---

## 一、小美同学能为你做什么?

### 📔 心情札记 - 构建你的数字分身

> 这是 XiaoMATE **最核心、最重要**的功能。你记录的每一篇札记，都是在为未来的"数字版自己"积累记忆。

**你的愿景:** 希望有一个完全了解自己的 AI，它记得你经历过什么、思考过什么、面对过什么。当你困惑时，它可以像另一个你一样给出建议；当你想分享自己的经验时，它可以替你与他人对话。

**小美的方案:**
- **全方位记录** - 工作进展、学习心得、生活琐事、情绪波动，统统可以写进札记
- **AI 自动整理** - 自动提取札记中的关键人物，建立你的**人物关系图谱**；分析心情标签，绘制情绪变化曲线
- **多维度回顾** - 支持**列表、日历、心情统计**多种视图，随时翻阅过去的自己
- **数字分身基础** - 随着记录积累，XiaoMATE 会越来越了解你。未来当你问"我曾经是怎么处理这类问题的？""我面对这种情况通常会怎么做？"时，它能基于你的真实经历给出属于"你自己"的答案
- **树洞与镜像** - 既是一个安全的倾诉空间，也是一面映照你成长轨迹的镜子
- 数据本地存储，隐私安全有保障

### 📚 书签收藏 - 再也不怕找不到好文章

**你的痛点:** 经常在微信、浏览器里看到感兴趣的文章,想着"待会儿再看",结果过几天想找时怎么都找不到了。

**小美的方案:**
- 看到好文章,随手转发到微信文件传输助手
- 隔几天一次性把链接批量添加到小美同学
- 小美会帮你把这些文章**全部下载保存到本地**,包括文章里的图片
- 保存格式是**大模型友好的 Markdown**,方便以后做知识库、AI 问答
- 支持按分类管理,支持关键词搜索,想什么时候看就什么时候看
- **卡片/列表双视图**自由切换,浏览方式随心选
- 支持**删除**和**重新下载**单篇收藏,管理更灵活

### ⏰ 待办提醒 - 私人事务,不上云才安心

**你的痛点:** 手头事情太多,各种待办工具一大堆,但私人信息不想记录到第三方软件、云服务器上。

**小美的方案:**
- 完全本地运行,**所有数据不上云**,隐私安全有保障
- 支持**一次性提醒**、**每日/每周/每月/每年循环提醒**
- 支持**公历/农历**两种日历,生日、节气、传统节日一个不落
- 到期后会在**系统右下角持续提醒你**,直到你确认关闭
- 除了桌面提醒,还支持自动推送到**企业微信、钉钉、飞书、邮件**

### 🤖 自动任务 - 让小美替你打工

**你的痛点:** 每天都要做的事情(天气预报、新闻、工作日报、周报、工时填报...), repetitive work 浪费时间。

**小美的方案:**
- 配置好任务,小美会自动定时执行,支持**一次性**或**循环执行**
- 可以配置**每天/每周/每月/每年**的执行频率,精确到星期几、几月几日
- 执行结果除了桌面提醒,同样支持推送到**企业微信、钉钉、飞书、邮件**
- 常见场景:
  - 每天自动获取天气预报
  - 每天推送你感兴趣领域的新闻
  - 自动填写工作日报/周报
  - 自动填报公司要求的每日工时
  - 任何你希望自动完成的 repetitive work

### 💬 AI 对话 - 你的 24 小时在线助理

- 双击桌宠即可打开聊天窗口
- 支持流式回复,**边想边说,不用等**
- 支持查看历史聊天记录
- 通过 WebSocket 实时连接,响应迅速

### 📸 截屏分析 - 让AI"看懂"你的屏幕

**你的痛点:** 看到报错信息不知道怎么解决,想快速了解屏幕上的内容,或者想知道当前打开了哪些应用。

**小美的方案:**
- 一键截屏,让AI帮你分析屏幕内容
- **常见用法:**
  - ✅ "帮我看看屏幕上打开了什么应用"
  - ✅ "识别屏幕上的所有文字内容"
  - ✅ "分析一下这个报错信息是什么问题"
  - ✅ "看看我现在的代码编辑器里写的是什么"
  - ✅ "屏幕上有几个窗口?分别是什么?"
- 适用于技术支持、文档整理、问题排查等场景

[![](https://oddmeta.net/docs/xiaomate/resources/screenshot-analyze-step2-returned-with-screenshot-and-analysis-progress.png)](http://oddmeta.net/docs/xiaomate/README.html)

[![](https://oddmeta.net/docs/xiaomate/resources/screenshot-analyze-step3-final-response-for-the-input.png)](http://oddmeta.net/docs/xiaomate/README.html)

### 🖼️ 照片分析 - 让AI"读懂"你的照片

**你的痛点:** 手机里有大量照片,想快速了解照片的拍摄时间、地点、内容等信息,但不想一张张翻看。

**小美的方案:**
- 把照片发给小美,AI会自动识别照片信息
- **常见问题:**
  - 📅 "看下这张照片是什么时候拍的?"
  - 📍 "这张照片拍摄地点是哪里?"
  - 🔍 "照片里有什么内容?"
- 支持分析照片EXIF信息(拍摄时间、设备、GPS位置等)
- 支持识别照片中的物体、场景、人物等内容

[![](https://oddmeta.net/docs/xiaomate/resources/xiaomate.chat.toolcall.png)](http://oddmeta.net/docs/xiaomate/README.html)

### 🎭 桌宠陪伴 - 可爱不只是花瓶

- **Live2D 2D 模型** 和 **VRM/GLB/GLTF 3D 模型** 双支持
- 拖动桌宠移动位置,移到屏幕边缘自动隐藏
- 右键打开圆盘菜单,双击打开聊天窗口
- 支持模型点击互动、待机动画、自动走动
- 支持透明区域点击穿透,**不挡着你用其他软件**

### 🎤 全局语音助手 - 唤醒即对话

**你的痛点:** 每次想和AI对话都需要打开聊天窗口，打字输入不够自然。

**小美的方案:**
- 🗣️ **语音唤醒**: 说出唤醒词（如"小美同学"），桌宠立即响应
- 🎙️ **语音对话**: 唤醒后直接说话，AI自动识别并回复
- 🔊 **TTS语音**: AI回复支持语音播报，不用盯着屏幕看
- 🌍 **全局待命**: 后台持续监听，不依赖聊天窗口
- 🔐 **自动认证**: 自动获取登录状态，无需重复登录

**使用场景:**
- 双手忙碌时，语音询问问题
- 开车、做饭时，语音交互
- 视力不佳的长辈，语音更方便
- 后台待命，随时呼唤

[![](https://oddmeta.net/docs/xiaomate/resources/voice-wakeup-demo.png)](http://oddmeta.net/docs/xiaomate/README.html)

---

## 二、快速开始

### 下载安装：推荐绿色免安装版体验，觉得对你有用再考虑安装

**Windows 用户:**
- 🟢 **绿色免安装版:** [下载 ZIP](https://github.com/oddmeta/xiaomate-desktop/releases/download/v2.2.21/xiaomate-v.2.2.21-portable-win64.zip)
  - 下载后解压缩,双击 `start.bat` 即可使用
- 📦 **安装包版:** [下载 EXE](https://github.com/oddmeta/xiaomate-desktop/releases/download/v2.2.21/xiaomate-v.2.2.21-setup-win64.zip)
  - 安装后可选开机自动启动

**Mac/Linux 用户:**
请自行下载代码,编译安装使用(见下方"开发者指南")

> 💡 **建议先试用绿色免安装版**,觉得好用再考虑用安装包安装

### 基本操作

| 操作 | 功能 |
| --- | --- |
| **拖动桌宠** | 移动窗口位置 |
| **单击模型** | 播放互动动画 |
| **右键桌宠** | 打开圆盘菜单 |
| **双击桌宠** | 打开/关闭聊天窗口 |
| **移至屏幕边缘** | 隐藏桌宠 |
| **单击边缘标签** | 恢复桌宠 |
| **右键系统托盘图标** | 打开显示、设置或退出菜单 |

---

## 三、功能详解

### 圆盘菜单

右键桌宠后,你会看到以下功能入口:

- 📌 **书签收藏** - 管理你收藏的文章
- 📔 **心情札记** - 记录日常，查看心情统计和人物关系
- ⏰ **提醒待办** - 查看和管理待办事项
- 🤖 **自动任务** - 配置自动化任务
- 🛠️ **技能说明** - 查看可用的 MCP 技能
- ⚙️ **设置** - 调整外观、行为、模型等
- 🔐 **登录** - 登录以使用在线功能
- 🚪 **退出** - 关闭小美同学

[![](https://oddmeta.net/docs/xiaomate/resources/xiaomate.menu.png)](http://oddmeta.net/docs/xiaomate/README.html)

> 未登录时,在线功能相关菜单会隐藏;登录后显示完整功能。

### 设置选项

右键桌宠 → 选择"设置",你可以调整:

- **网络** - 后端服务地址
- **外观** - 桌宠大小、窗口边框、待机动画
- **行为** - 点击穿透、自动走动参数
- **模型** - 扫描、切换内置模型
- **边缘** - 边缘隐藏行为
- **系统** - 开机自启、调试模式

保存设置后,会立即生效。

---

## 四、开发者指南

### 环境要求

- **Node.js:** >= 18.0.0 (LTS 版本)
- **npm:** >= 9.0.0
- **操作系统:** Windows 10/11, macOS 10.15+, Linux

### 从源码启动

```bash
# 克隆仓库
git clone https://github.com/oddmeta/xiaomate-desktop.git
cd xiaomate-desktop

# 安装依赖
npm install

# 启动开发环境
npm start
```

**Windows:** 也可直接运行 `start.bat`

**macOS/Linux:**
```bash
chmod +x start.sh
./start.sh
```

### 语音功能开发提示

如果你要开发或调试语音功能：

1. **确保后端服务已启动**
   ```bash
   # Windows
   cd ..\xiaoluo
   python xiaoluo_app.py
   
   # macOS/Linux
   cd ../xiaoluo
   python xiaoluo_app.py
   ```

2. **查看主进程日志**
   - 启动后会看到 `[语音助手]` 相关日志
   - 检查是否成功获取 `session_id`

3. **查看渲染进程日志**
   - 打开 DevTools (F12)
   - 查看 `[语音UI]` 和 `[聊天]` 日志

4. **语音模块位置**
   - 代码位于 `lib/pet-voice/`
   - 文档位于 `docs/VOICE_ASSISTANT_REFACTOR.md`

### 构建发布

**Windows:**
```bash
npm run build
# 或
build.bat
```
生成: `release/XiaoMate_vX.X.X_YYYY-MM-DD.exe` (NSIS 安装包)

**macOS:**
```bash
npm run build
# 或
./build.sh
```
生成: `release/XiaoMate_vX.X.X_YYYY-MM-DD.dmg` + `.zip`

**Linux:**
```bash
npm run build
# 或
./build.sh
```
生成: `release/XiaoMate_vX.X.X_YYYY-MM-DD.AppImage` + `.deb` + `.rpm`

> ⚠️ **Windows 构建前请关闭本项目及其他 Electron 应用**

---

## 五、项目信息

- **当前版本:** v2.4.32
- **应用 ID:** `com.oddmeta.xiaomate`
- **代码仓库:** https://github.com/oddmeta/xiaomate-desktop
- **发布页面:** https://github.com/oddmeta/xiaomate-desktop/releases
- **后端项目:** https://github.com/catherine-wei/learning-ai
- **帮助文档:** https://oddmeta.net/docs/xiaomate

---

## 六、技术架构(供开发者参考)

小美同学基于 Electron 构建,支持 Windows/macOS/Linux 跨平台运行。核心特性:

### 前端架构

- **模型渲染:** PIXI.js + Live2D Cubism 4 (2D), Three.js + VRM 运行时 (3D)
- **UI框架:** 原生 HTML/CSS/JavaScript，轻量化设计
- **通信协议:** WebSocket 实时连接,支持流式 AI 回复
- **本地存储:** 所有用户配置数据保存在本地用户目录
  - Windows: `%APPDATA%\XiaoMate\pet-config.json`
  - macOS: `~/Library/Application Support/XiaoMate/pet-config.json`
  - Linux: `~/.config/XiaoMate/pet-config.json` 
- **认证机制:** 基于 Electron Session Cookie 的登录认证
- **动画支持:** VRM 内置动画、VRMA 文件、FBX 动画

### 语音助手架构 (新增)

```
lib/pet-voice/                    ← 全局语音助手模块
├── index.js                      ← 统一导出入口
├── voice-assistant.js            ← 主进程核心（WebSocket、认证、状态管理）
├── voice-integration.js          ← 初始化入口和IPC处理器
├── audio-capture.js              ← 系统音频采集
├── kws-bridge.js                 ← KWS唤醒检测桥接
└── README.md                     ← 模块文档
```

**语音数据流:**
```
用户说话 → AudioCapture采集 → KWS Bridge发送(携带session_id) 
→ 后端ASR识别 → 后端LLM处理 → 前端显示识别结果 → 前端流式显示AI回复 → TTS播放
```

**核心特性:**
- ✅ **认证自动传递**: 主进程从Electron session获取cookie，WebSocket连接自动携带
- ✅ **全局待命**: 后台持续监听，不依赖渲染进程
- ✅ **状态统一管理**: 主进程维护单一状态，通过IPC同步到渲染进程
- ✅ **进程隔离**: 主进程管理网络/音频，渲染进程负责UI，崩溃不影响语音服务

### 模块结构

```
frontend-desktop/
├── main.js                       ← Electron主进程
├── preload.js                    ← 预加载脚本（安全暴露IPC）
├── voice-ui.js                   ← 渲染进程语音UI
├── lib/
│   ├── pet-voice/                ← 🆕 语音助手模块
│   ├── pet-chat.js               ← 聊天功能
│   ├── pet-model-*.js            ← 模型渲染
│   ├── pet-notifications.js      ← 通知系统
│   └── ...                       ← 其他功能模块
├── docs/                         ← 技术文档
│   ├── VOICE_ASSISTANT_REFACTOR.md
│   ├── FIX_VOICE_TRANSCRIPT_DISPLAY.md
│   └── MIGRATION_PET_VOICE.md
└── resources/                    ← 静态资源
```

详细技术文档请查看:
- [跨平台运行指南](docs/CROSS_PLATFORM.md)
- [快速启动指南](docs/QUICKSTART.md)
- [FBX 动画集成说明](docs/FBX-动画集成说明.md)
- [全局语音助手架构](docs/VOICE_ASSISTANT_REFACTOR.md) 🆕
- [语音文本显示修复](docs/FIX_VOICE_TRANSCRIPT_DISPLAY.md) 🆕
- [语音模块迁移说明](docs/MIGRATION_PET_VOICE.md) 🆕

---

## 七、常见问题

**Q: 需要联网才能使用吗?**

A: 桌宠显示、模型渲染、本地设置等可以离线使用。AI 对话、书签下载、在线提醒等功能需要连接 XiaoMate 后端服务。

**Q: 数据安全吗?**

A: 待办提醒、自动任务等数据完全本地存储,不上云。在线功能的数据存储在后端服务器,建议自行搭建后端服务以保证隐私。

**Q: 可以自己添加模型吗?**

A: 可以!在设置 → 模型中扫描你的模型目录,支持 Live2D `.model3.json` 和 VRM/GLB/GLTF 格式。

**Q: 支持哪些通知渠道?**

A: 支持桌面通知、企业微信、钉钉、飞书、邮件推送。

**Q: 如何使用语音唤醒功能?**

A: 1. 确保已登录并连接到后端服务
    2. 在设置中启用“语音唤醒”
    3. 说出唤醒词（如“小美同学”）
    4. 唤醒后直接说话即可

**Q: 语音唤醒需要联网吗?**

A: 是的，语音识别(ASR)和大模型(LLM)需要连接后端服务。音频采集和唤醒词检测(KWS)可以离线运行。

**Q: 关闭聊天窗口后，语音服务还在运行吗?**

A: 是的！语音服务在主进程运行，不依赖渲染进程。关闭聊天窗口后仍可语音唤醒。

---

**感谢使用 XiaoMATE 小美同学! 🎉**

如有问题或建议,欢迎在 [GitHub Issues](https://github.com/oddmeta/xiaomate-desktop/issues) 反馈。
也欢迎你关注我的个人公众号：奥德元。