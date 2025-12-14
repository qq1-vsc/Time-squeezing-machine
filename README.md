# 执剑人系统 - 时间压榨机器 v2.0

## 🎯 项目简介

AI 驱动的极限效率时间管理系统。使用 DeepSeek API 进行疯狂计划优化，实时执行跟踪，自动数据持久化和分析。

---

## ✨ 核心功能

| 功能 | 说明 |
|------|------|
| 🤖 **疯狂优化** | DeepSeek API 驱动的计划优化，生成 S/A/B 优先级任务 |
| ⏱️ **实时执行** | 实时计时器、倒计时、任务级动态监测、AI 实时指导 |
| 📊 **动态监测** | 每个任务显示提前完成/按时/超时状态，倒计时进入负计时 |
| 💾 **数据持久化** | SQLite 自动保存所有计划和任务记录 |
| 📈 **数据分析** | 30 天趋势图表、完成率统计、CSV 导出 |
| 🔄 **继续功能** | 继续上一次或今天的计划，智能恢复 |
| 🔑 **API 管理** | API Key 本地保存，一次配置永久有效 |
| 📱 **网络访问** | 支持本地和局域网（手机/平板）访问 |

---

## 🚀 快速开始

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 启动应用
**推荐方式：** 双击 `一键启动.bat`

或手动启动：
```bash
streamlit run app_v2.py
```

### 3. 打开应用
- 本地访问：`http://localhost:8501`
- 网络访问：`http://你的IP:8501`

---

## 📚 使用说明

### 首次使用

1. **启动应用** → 双击 `一键启动.bat`
2. **配置 API Key**（仅需一次）：
   - 访问 https://platform.deepseek.com 获取 API Key
   - 在左侧边栏输入并保存
   - 系统自动保存到本地配置文件
3. **后续使用** → API Key 自动加载，无需重复输入

### 标准工作流

```
1. 输入你的计划/任务
2. 点击"疯狂优化"
3. 查看 AI 优化的计划
4. 点击"开始执行计划"
5. 逐一完成任务：
   - 显示提前完成 (⭐ 节省时间)
   - 显示按时完成 (✅)
   - 显示超时完成 (⚠️ 超时 Xm Xs)
6. 倒计时为负时变危险红色 (🔴)
7. 系统自动保存所有数据
8. 在"数据面板"查看统计
```

### 任务级动态监测

每个任务完成时系统会判断：
- **进行中** → ⏳ 绿色显示
- **提前完成** → ⭐ 节省时间提示
- **按时完成** → ✅ 确认状态
- **超时完成** → ⚠️ 显示超时时间
- **严重超时** → 🔴 危险红色倒计时

### 数据面板三大功能

| 选项卡 | 功能 |
|-------|------|
| **今日统计** | 优先级分布、时间分配、关键指标 |
| **历史趋势** | 30 天时间对比、专注度、完成率曲线 |
| **所有计划** | 计划列表、详细统计、CSV 导出 |

### 继续上一次计划

侧边栏 → "▶️ 继续上一次" 或 "▶️ 继续今天"

---

## 📂 文件结构

```
.
├── app_v2.py                    # 主应用程序
├── data_manager.py              # 数据库管理模块
├── config_manager.py            # 配置管理（API Key 持久化）
├── requirements.txt             # Python 依赖
├── wallfacer_data.db           # SQLite 数据库（自动生成）
├── config.json                  # 本地配置文件（自动生成）
├── 一键启动.bat                 # 启动脚本
└── 一键同步到GitHub.bat         # GitHub 同步脚本
```

---

## 🔧 技术栈

- **前端框架**：Streamlit
- **AI 模型**：DeepSeek API（OpenAI 兼容）
- **数据存储**：SQLite
- **数据分析**：Pandas、Plotly
- **语言**：Python 3.7+

---

## � API Key 管理

### 一劳永逸配置

1. **首次启动** → 在左侧边栏展开 "API Key 配置"
2. **输入 API Key** → 从 https://platform.deepseek.com 获取
3. **保存** → 点击 "✅ 保存并测试"
4. **后续使用** → 系统自动加载，无需重复输入

### 配置文件位置

API Key 保存在：`config.json`

```json
{
  "deepseek_api_key": "your_api_key_here"
}
```

### 更新 API Key

在左侧边栏点击 "🔄 更新 API Key"，然后输入新的 Key

---

## 🔄 GitHub 同步

### 快速上传

修改代码后，双击 `一键同步到GitHub.bat`

1. 输入提交描述
2. 自动推送到 GitHub

---

## ❓ 常见问题

### Q: API Key 忘了怎么办？
**A:** API Key 保存在 `config.json` 中，可以直接编辑或在应用中更新

### Q: 启动脚本无反应？
**A:** 运行 `python --version` 检查 Python 是否安装，然后手动运行 `streamlit run app_v2.py`

### Q: 如何在手机上访问？
**A:** 
1. 查询电脑 IP：`ipconfig` 找 IPv4 地址
2. 在手机浏览器访问：`http://电脑IP:8501`

### Q: 数据会丢失吗？
**A:** 不会。所有数据保存在 `wallfacer_data.db`，可以备份此文件

### Q: 如何修改 AI 优化的强度？
**A:** 编辑 `app_v2.py` 中的 API 提示词（搜索 `"请为我疯狂优化"`）

### Q: 能否离线使用？
**A:** 不能。实时优化功能需要 DeepSeek API 连接

---

## 📊 数据库架构

### 三个核心表

**plans** - 计划表
```sql
id, date, title, total_minutes, tasks_json, status, created_at
```

**task_records** - 任务记录表
```sql
id, plan_id, task_name, scheduled_minutes, actual_minutes, 
focus_level, completed, completed_at, notes
```

**daily_logs** - 日志表
```sql
id, date, total_scheduled, total_actual, completion_rate, 
avg_focus, notes, created_at
```

---

## 🎯 特色功能说明

### AI 疯狂优化
- 输入原始计划
- DeepSeek 自动重新排序和分解
- 生成 S/A/B 三级优先级
- 优化时间分配

### 实时执行模式
- 实时计时器（精确到秒）
- 三色倒计时（绿→橙→红）
- 实时 AI 对话指导
- 任务切换和时间调整

### 数据持久化
- 每次计划开始自动保存
- 每个任务完成记录详情
- 每天生成日志汇总
- 支持任意恢复和查询

---

## 🚀 未来计划

- [ ] 周/月报表生成
- [ ] 团队协作功能
- [ ] 移动应用（Flutter/React Native）
- [ ] 云同步和备份
- [ ] 自定义主题和皮肤
- [ ] 集成日历视图

---

## 📝 许可证

MIT License - 自由使用和修改

---

**祝你使用愉快！** ⚡

然后在手机浏览器访问: `http://[电脑IP地址]:8501`

**查看电脑 IP 地址:**
- Windows: 打开 CMD，输入 `ipconfig`
- Mac/Linux: 终端输入 `ifconfig` 或 `ip addr`

## 获取 Gemini API Key

1. 访问 [Google AI Studio](https://aistudio.google.com/app/apikey)
2. 登录 Google 账号
3. 点击 "Create API Key"
4. 复制 API Key

## 技术栈

- **Python** - 核心语言
- **Streamlit** - Web 框架
- **Google Gemini API** - AI 能力
- **Pandas** - 数据处理
- **Plotly** - 数据可视化

## 文件结构

```
Wallfacer System/
├── app.py              # 主应用文件
├── requirements.txt    # 依赖列表
├── README.md           # 说明文档
├── run.bat             # Windows 快速启动脚本
├── run_mobile.bat      # Windows 局域网启动脚本
└── wallfacer_data.csv  # 数据文件 (自动生成)
```

## 许可

MIT License

---

*"弱小和无知不是生存的障碍，傲慢才是。"* —— 《三体》
