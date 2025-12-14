# GitHub 上传教程 | 执剑人系统 v2.0

## 📚 目录
1. [初始化 Git 仓库](#初始化-git-仓库)
2. [上传到 GitHub](#上传到-github)
3. [后续更新](#后续更新)
4. [常见命令](#常见命令)

---

## 初始化 Git 仓库

### 步骤 1: 安装 Git
- 访问 [git-scm.com](https://git-scm.com/)
- 下载并安装 Git

### 步骤 2: 配置 Git
打开 PowerShell，输入：

```powershell
git config --global user.name "你的名字"
git config --global user.email "你的邮箱@example.com"
```

### 步骤 3: 初始化本地仓库
在项目目录创建 `.gitignore` 文件：

```powershell
cd "e:\Wallfacer System"

# 创建 .gitignore
@"
__pycache__/
*.pyc
.streamlit/secrets.toml
wallfacer_data.db
*.csv
.env
.venv/
venv/
"@ | Out-File -Encoding UTF8 .gitignore

# 初始化 Git
git init
```

### 步骤 4: 提交第一次代码
```powershell
git add .
git commit -m "初始化: 执剑人系统 v2.0 - 时间压榨机器"
```

---

## 上传到 GitHub

### 步骤 1: 创建 GitHub 仓库

1. 登录 [GitHub](https://github.com)
2. 点击右上角 `+` → `New repository`
3. 填写信息：
   - **Repository name**: `wallfacer-system` (或你喜欢的名字)
   - **Description**: `极致效率的 AI 时间管理工具 | AI-driven time management app`
   - **Public** (如果想分享) 或 **Private** (私人)
   - 不要选择 "Initialize with README" (因为本地已有代码)
4. 点击 `Create repository`

### 步骤 2: 连接远程仓库

GitHub 创建后会显示命令，在本地运行：

```powershell
cd "e:\Wallfacer System"

# 添加远程仓库
git remote add origin https://github.com/你的用户名/wallfacer-system.git

# 修改分支名（如需要）
git branch -M main

# 推送代码
git push -u origin main
```

### 步骤 3: 验证上传
- 访问 `https://github.com/你的用户名/wallfacer-system`
- 确认代码已上传

---

## 后续更新

### 每次修改后同步到 GitHub

```powershell
cd "e:\Wallfacer System"

# 查看变更
git status

# 暂存所有更改
git add .

# 提交变更（写清楚修改说明）
git commit -m "功能: 添加数据分析面板 | 优化任务执行流程"

# 推送到 GitHub
git push
```

### 常见的 commit 消息格式

```
feat: 新功能（如：feat: 添加实时倒计时）
fix: 修复（如：fix: 修复进度条显示错误）
docs: 文档（如：docs: 更新 README）
style: 代码风格（如：style: 统一缩进）
refactor: 重构（如：refactor: 优化数据管理模块）
test: 测试（如：test: 添加单元测试）
chore: 其他（如：chore: 更新依赖）
```

---

## 常见命令

### 查看日志
```powershell
git log --oneline  # 查看提交历史
git log --graph --oneline --all  # 图形化显示
```

### 撤销操作
```powershell
git restore <file>  # 撤销文件修改
git reset HEAD~1  # 撤销最后一次提交（保留更改）
git revert <commit>  # 创建新提交来撤销指定提交
```

### 分支管理
```powershell
git branch  # 查看本地分支
git branch -a  # 查看所有分支
git checkout -b <branch-name>  # 创建并切换分支
git switch main  # 切换回主分支
```

### 同步远程更新
```powershell
git fetch origin  # 获取远程更新
git pull origin main  # 拉取并合并远程代码
```

---

## 📌 创建 README 文件

在项目根目录创建 `README.md`：

```markdown
# ⚡ 执剑人系统 v2.0 | 时间压榨机器

## 功能特性

### 🎯 计划优化
- AI 激进优化你的计划
- 自动分解成微任务（≤25分钟）
- 标注优先级和学习价值

### ⏱️ 实时执行
- 倒计时显示（三阶段视觉反馈）
- 实时 AI 对话调整方案
- 详细的时间追踪

### 📊 数据分析
- 30天历史趋势分析
- 完成率、专注度统计
- 一键导出 CSV

### 💾 数据持久化
- 所有计划自动保存
- 支持继续上一次计划
- 任务执行记录完整追踪

## 快速开始

### 安装依赖
```bash
pip install -r requirements.txt
```

### 启动应用
```bash
streamlit run app_v2.py
```

### 配置 API
1. 访问 [platform.deepseek.com](https://platform.deepseek.com)
2. 获取 API Key
3. 在应用侧边栏粘贴并启动

## 技术栈

- **Python** - 核心语言
- **Streamlit** - Web 框架
- **DeepSeek API** - AI 能力
- **SQLite** - 数据持久化
- **Plotly** - 数据可视化
- **Pandas** - 数据处理

## 项目结构

```
wallfacer-system/
├── app_v2.py              # 主应用
├── data_manager.py        # 数据管理模块
├── requirements.txt       # 依赖列表
├── README.md              # 说明文档
├── run_v2.bat             # Windows 启动脚本
├── .streamlit/            # Streamlit 配置
└── wallfacer_data.db      # 数据库（自动生成）
```

## 使用流程

1. **输入计划** - 描述今天的所有事项
2. **疯狂优化** - AI 激进优化计划
3. **开始执行** - 进入实时执行模式
4. **实时调整** - 通过对话修改方案
5. **数据分析** - 查看历史趋势

## 许可

MIT License

---

**"不要浪费每一秒，每一秒都是成长的机会"** ⚡
```

### 上传 README
```powershell
git add README.md
git commit -m "docs: 添加项目说明文档"
git push
```

---

## 🎯 建议

1. **定期提交** - 每完成一个功能就提交一次
2. **清晰的 commit 信息** - 便于以后回顾
3. **GitHub Pages** - 可以为项目添加展示页面
4. **Issues & Discussions** - 记录 Bug 和想法
5. **Star & Fork** - 让更多人了解你的项目

---

## ❓ 常见问题

### Q: 如何修改已提交的代码？
```powershell
# 修改最后一次提交
git add .
git commit --amend

# 修改历史提交（谨慎操作）
git rebase -i HEAD~3
```

### Q: 如何恢复已删除的文件？
```powershell
git restore <file>
```

### Q: 如何忽略某些文件？
编辑 `.gitignore` 文件，添加规则。

---

祝你效率提升！🚀
