# 时间压榨机器 v2.0

AI 驱动的极限效率时间管理系统。

## 快速开始

```bash
# 安装依赖
pip install -r requirements.txt

# 启动应用
双击 一键启动.bat
# 或手动运行
streamlit run app_v2.py
```

访问：http://localhost:8501

## 核心功能

| 功能 | 说明 |
|------|------|
| **疯狂优化** | DeepSeek API 驱动的计划优化 |
| **实时执行** | 倒计时、超时警告、负计时 |
| **动态监测** | 提前/按时/超时完成提示 |
| **数据持久化** | SQLite 自动保存 |
| **继续计划** | 支持继续上一次/今天的计划 |

## 使用流程

```
1. 首次使用：左侧边栏输入 API Key（仅一次）
2. 输入计划 → 点击「疯狂优化」
3. 查看优化结果 → 点击「开始执行」
4. 完成任务 → 点击「✅ 完成任务」
   - 提前完成：显示节省时间 ⭐
   - 超时完成：显示超出时间 ⚠️
   - 负计时：危险红色闪烁 🔴
5. 在「数据面板」查看统计
```

## 文件说明

```
app_v2.py           # 主应用
data_manager.py     # 数据库管理
config_manager.py   # API Key 持久化
requirements.txt    # 依赖
config.json         # 本地配置（自动生成）
wallfacer_data.db   # 数据库（自动生成）
```

## API Key 配置

- 获取：https://platform.deepseek.com
- 首次：在侧边栏输入并保存
- 后续：自动加载，无需重复输入

## 常见问题

**Q: 继续上一次报错？**  
A: 已修复，现在兼容旧数据格式

**Q: 手机访问？**  
A: 访问 http://电脑IP:8501

**Q: 数据备份？**  
A: 备份 `wallfacer_data.db` 和 `config.json`

## 技术栈

Streamlit + DeepSeek API + SQLite + Plotly

---

**双击 一键启动.bat 开始使用！**
