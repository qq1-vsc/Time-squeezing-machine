# -*- coding: utf-8 -*-
"""
Wallfacer System (执剑人系统)
AI-Driven Personal Management Dashboard
Tech Stack: Python, Streamlit, DeepSeek API, Pandas, Plotly
"""

import streamlit as st
from openai import OpenAI
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import os
from datetime import datetime
import time
from functools import wraps

# ============================================
# 1. 系统初始化与配置
# ============================================

# 页面配置
st.set_page_config(
    page_title="Wallfacer System | 执剑人系统",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义 CSS - 极简科技感风格
st.markdown("""
<style>
    /* 主题颜色 */
    :root {
        --primary-color: #00d4ff;
        --bg-dark: #0a0a0f;
        --card-bg: #1a1a2e;
    }
    
    /* 全局样式 */
    .stApp {
        background: linear-gradient(135deg, #0a0a0f 0%, #1a1a2e 100%);
    }
    
    /* 标题样式 */
    h1, h2, h3 {
        color: #00d4ff !important;
        font-family: 'Consolas', monospace;
    }
    
    /* 卡片样式 */
    .metric-card {
        background: linear-gradient(145deg, #1a1a2e, #16213e);
        border: 1px solid #00d4ff33;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.1);
    }
    
    /* 评分显示 */
    .score-display {
        font-size: 72px;
        font-weight: bold;
        color: #00d4ff;
        text-align: center;
        text-shadow: 0 0 30px rgba(0, 212, 255, 0.5);
    }
    
    /* 执剑人评语 */
    .swordholder-quote {
        font-style: italic;
        color: #888;
        border-left: 3px solid #00d4ff;
        padding-left: 15px;
        margin: 20px 0;
    }
    
    /* 按钮样式 */
    .stButton > button {
        background: linear-gradient(90deg, #00d4ff, #0099cc);
        color: #0a0a0f;
        border: none;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.5);
        transform: translateY(-2px);
    }
    
    /* 侧边栏 */
    .css-1d391kg {
        background: #0a0a0f;
    }
    
    /* 进度条 */
    .stProgress > div > div {
        background: linear-gradient(90deg, #00d4ff, #00ff88);
    }
</style>
""", unsafe_allow_html=True)

# 数据文件路径
DATA_FILE = "wallfacer_data.csv"

# ============================================
# Session State 初始化
# ============================================
def init_session_state():
    """初始化所有需要的 session state 变量"""
    if 'api_key' not in st.session_state:
        st.session_state.api_key = ""
    if 'api_configured' not in st.session_state:
        st.session_state.api_configured = False
    if 'task_list' not in st.session_state:
        st.session_state.task_list = []
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'today_score' not in st.session_state:
        st.session_state.today_score = None
    if 'today_comment' not in st.session_state:
        st.session_state.today_comment = None
    if 'model' not in st.session_state:
        st.session_state.model = None

init_session_state()

# ============================================
# DeepSeek API 配置
# ============================================
def configure_deepseek(api_key: str) -> bool:
    """配置 DeepSeek API"""
    try:
        client = OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com"
        )
        # 测试连接
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": "Hi"}],
            max_tokens=10
        )
        st.session_state.client = client
        st.session_state.api_configured = True
        st.session_state.api_key = api_key
        return True
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg or "quota" in error_msg.lower():
            st.error(f"⚠️ API 配额已超限\n\n{error_msg}")
        elif "401" in error_msg or "invalid" in error_msg.lower():
            st.error(f"⚠️ API Key 无效，请检查是否正确\n\n{error_msg}")
        else:
            st.error(f"API 配置失败: {error_msg}")
        st.session_state.api_configured = False
        return False

def call_deepseek(system_prompt: str, user_input: str) -> str:
    """调用 DeepSeek API，带有重试和速率限制"""
    if not st.session_state.api_configured:
        raise Exception("API 未配置")
    
    max_retries = 3
    retry_delay = 2  # 初始延迟时间（秒）
    
    for attempt in range(max_retries):
        try:
            # 添加请求间隔
            if attempt > 0:
                time.sleep(retry_delay)
            
            response = st.session_state.client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ],
                stream=False
            )
            return response.choices[0].message.content
            
        except Exception as e:
            error_msg = str(e)
            
            # 检查是否是配额超限错误 (429)
            if "429" in error_msg or "quota" in error_msg.lower() or "exceeded" in error_msg.lower():
                if attempt < max_retries - 1:
                    wait_time = retry_delay * (2 ** attempt)  # 指数退避
                    st.warning(f"⚠️ API 配额已满，将在 {wait_time} 秒后重试... ({attempt + 1}/{max_retries})")
                    time.sleep(wait_time)
                    continue
                else:
                    raise Exception(
                        f"❌ API 配额已超限\n\n"
                        f"原因: {error_msg}\n\n"
                        f"解决方案:\n"
                        f"1. 稍后再试\n"
                        f"2. 充值 DeepSeek 账户\n"
                        f"3. 访问: https://platform.deepseek.com 查看配额信息"
                    )
            else:
                # 其他错误直接抛出
                raise Exception(f"API 调用失败: {error_msg}")

# ============================================
# 数据持久化函数
# ============================================
def save_to_csv(score: int, comment: str):
    """保存数据到 CSV 文件"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_data = pd.DataFrame([{
        'timestamp': timestamp,
        'date': datetime.now().strftime("%Y-%m-%d"),
        'score': score,
        'comment': comment
    }])
    
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        df = pd.concat([df, new_data], ignore_index=True)
    else:
        df = new_data
    
    df.to_csv(DATA_FILE, index=False, encoding='utf-8-sig')

def load_from_csv() -> pd.DataFrame:
    """从 CSV 文件加载数据"""
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    return pd.DataFrame(columns=['timestamp', 'date', 'score', 'comment'])

# ============================================
# 侧边栏 - API 配置
# ============================================
with st.sidebar:
    st.markdown("## 🌌 执剑人系统")
    st.markdown("---")
    
    st.markdown("### ⚙️ API 配置")
    
    # 尝试从 secrets 获取 API Key
    default_key = ""
    try:
        if hasattr(st, 'secrets') and 'DEEPSEEK_API_KEY' in st.secrets:
            default_key = st.secrets['DEEPSEEK_API_KEY']
    except:
        pass
    
    api_key_input = st.text_input(
        "DeepSeek API Key",
        type="password",
        value=st.session_state.api_key or default_key,
        help="输入你的 DeepSeek API Key (从 platform.deepseek.com 获取)"
    )
    
    if st.button("🔗 连接 API", use_container_width=True):
        if api_key_input:
            with st.spinner("正在连接..."):
                if configure_deepseek(api_key_input):
                    st.success("✅ API 连接成功!")
                else:
                    st.error("❌ 连接失败")
        else:
            st.warning("请输入 API Key")
    
    # 显示连接状态
    if st.session_state.api_configured:
        st.markdown("🟢 **状态: 已连接**")
    else:
        st.markdown("🔴 **状态: 未连接**")
    
    st.markdown("---")
    
    # 配额使用提示
    with st.expander("💡 配额使用提示", expanded=False):
        st.markdown("""
        **DeepSeek API 优势:**
        - 价格便宜 (约 $0.14/百万 tokens)
        - 配额充足，很少限流
        - 中文理解能力强
        
        **获取 API Key:**
        1. 访问: https://platform.deepseek.com
        2. 注册并充值
        3. 创建 API Key
        """)
    
    st.markdown("---")
    
    # 局域网访问说明
    st.markdown("### 📱 手机访问")
    st.markdown("""
    在终端运行:
    ```
    streamlit run app.py --server.address 0.0.0.0
    ```
    然后用手机浏览器访问:
    `http://[电脑IP]:8501`
    """)
    
    st.markdown("---")
    st.markdown("*给岁月以文明，而不是给文明以岁月*")

# ============================================
# 主页面标题
# ============================================
st.markdown("""
<div style="text-align: center; padding: 20px 0;">
    <h1 style="font-size: 3em; margin-bottom: 0;">🌌 WALLFACER SYSTEM</h1>
    <p style="color: #666; font-size: 1.2em;">执剑人系统 | AI 驱动的个人管理仪表盘</p>
</div>
""", unsafe_allow_html=True)

# ============================================
# 主要功能模块 - 使用 Tabs
# ============================================
tab1, tab2, tab3 = st.tabs(["📋 战略规划", "🧠 状态监测", "📊 历史仪表盘"])

# ============================================
# 模块一：战略规划 (Strategic Planning)
# ============================================
with tab1:
    st.markdown("## 📋 战略规划 | Strategic Planning")
    st.markdown("*将混沌的思绪转化为清晰的执行路径*")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📝 输入今日计划")
        user_plan = st.text_area(
            "描述你今天想做的事情",
            height=200,
            placeholder="例如：今天要看完计算机体系结构第三章，还要写完Verilog实验报告，顺便去取个快递...",
            key="plan_input"
        )
        
        if st.button("🔮 面壁者思考 (Analyze Plan)", use_container_width=True, type="primary"):
            if not st.session_state.api_configured:
                st.error("⚠️ 请先在侧边栏配置 API Key")
            elif not user_plan.strip():
                st.warning("请输入今日计划")
            else:
                with st.spinner("面壁者正在深度思考..."):
                    try:
                        system_prompt = """你是一个任务管理专家。请将用户的自然语言描述转化为一个JSON格式的任务列表。
每个任务包含:
- 'task': 任务名称 (string)
- 'estimated_time': 预估时间，如 "30分钟", "2小时" (string)
- 'priority': 优先级 (string): "High", "Medium", "Low"
- 'completed': 是否完成 (boolean): 默认为 false

只输出纯 JSON 数组，不要包含 markdown 代码块标记，不要输出任何其他文字。
示例格式: [{"task": "xxx", "estimated_time": "1小时", "priority": "High", "completed": false}]"""
                        
                        response = call_deepseek(system_prompt, user_plan)
                        
                        # 清理响应，移除可能的 markdown 代码块标记
                        cleaned_response = response.strip()
                        if cleaned_response.startswith("```"):
                            cleaned_response = cleaned_response.split("\n", 1)[1]
                        if cleaned_response.endswith("```"):
                            cleaned_response = cleaned_response.rsplit("```", 1)[0]
                        cleaned_response = cleaned_response.strip()
                        
                        # 解析 JSON
                        task_list = json.loads(cleaned_response)
                        
                        # 确保每个任务都有 completed 字段
                        for task in task_list:
                            if 'completed' not in task:
                                task['completed'] = False
                        
                        st.session_state.task_list = task_list
                        st.success("✅ 任务解析成功!")
                        
                    except json.JSONDecodeError as e:
                        st.error(f"❌ JSON 解析失败: {str(e)}")
                        st.code(response, language="text")
                    except Exception as e:
                        st.error(str(e))
    
    with col2:
        st.markdown("### 📊 任务清单")
        
        if st.session_state.task_list:
            # 计算完成进度
            total_tasks = len(st.session_state.task_list)
            completed_tasks = sum(1 for t in st.session_state.task_list if t.get('completed', False))
            progress = completed_tasks / total_tasks if total_tasks > 0 else 0
            
            # 显示进度
            st.markdown(f"**完成进度: {completed_tasks}/{total_tasks}**")
            st.progress(progress)
            
            # 显示任务列表
            for i, task in enumerate(st.session_state.task_list):
                col_check, col_task, col_time, col_priority = st.columns([0.5, 3, 1.5, 1])
                
                with col_check:
                    checked = st.checkbox(
                        "",
                        value=task.get('completed', False),
                        key=f"task_check_{i}"
                    )
                    st.session_state.task_list[i]['completed'] = checked
                
                with col_task:
                    task_style = "text-decoration: line-through; color: #666;" if checked else ""
                    st.markdown(f"<span style='{task_style}'>{task['task']}</span>", unsafe_allow_html=True)
                
                with col_time:
                    st.markdown(f"⏱️ {task['estimated_time']}")
                
                with col_priority:
                    priority_colors = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}
                    st.markdown(priority_colors.get(task['priority'], "⚪") + f" {task['priority']}")
            
            # 清空任务按钮
            if st.button("🗑️ 清空任务列表"):
                st.session_state.task_list = []
                st.rerun()
        else:
            st.info("💡 在左侧输入今日计划，让面壁者为你分析任务")

# ============================================
# 模块二：生理与心理监测 (Bio-State Monitoring)
# ============================================
with tab2:
    st.markdown("## 🧠 状态监测 | Bio-State Monitoring")
    st.markdown("*执剑人将审视你的生理与心理状态*")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📝 描述你的状态")
        user_state = st.text_area(
            "描述今天的身体/精神状态",
            height=200,
            placeholder="例如：昨晚熬夜了，现在头有点昏，但是精神很亢奋...",
            key="state_input"
        )
        
        if st.button("⚔️ 执剑人裁决 (Evaluate)", use_container_width=True, type="primary"):
            if not st.session_state.api_configured:
                st.error("⚠️ 请先在侧边栏配置 API Key")
            elif not user_state.strip():
                st.warning("请描述你的状态")
            else:
                with st.spinner("执剑人正在审视..."):
                    try:
                        system_prompt = """你是一个严格的健康分析师，同时也是刘慈欣《三体》中的执剑人。
根据用户的描述，你需要:
1. 给出一个 '状态评分' (0-100整数)
2. 给出一段简短犀利的 '执剑人评语' (风格参考《三体》，冷酷但富有哲理，不超过50字)

只输出纯 JSON，格式如下，不要包含 markdown 代码块标记:
{"score": 75, "comment": "你的评语..."}

不要输出任何其他内容。"""
                        
                        response = call_deepseek(system_prompt, user_state)
                        
                        # 清理响应
                        cleaned_response = response.strip()
                        if cleaned_response.startswith("```"):
                            cleaned_response = cleaned_response.split("\n", 1)[1]
                        if cleaned_response.endswith("```"):
                            cleaned_response = cleaned_response.rsplit("```", 1)[0]
                        cleaned_response = cleaned_response.strip()
                        
                        # 解析 JSON
                        result = json.loads(cleaned_response)
                        score = int(result['score'])
                        comment = result['comment']
                        
                        # 保存到 session state
                        st.session_state.today_score = score
                        st.session_state.today_comment = comment
                        
                        # 保存到 CSV
                        save_to_csv(score, comment)
                        
                        st.success("✅ 裁决完成!")
                        
                    except json.JSONDecodeError as e:
                        st.error(f"❌ JSON 解析失败: {str(e)}")
                        st.code(response, language="text")
                    except Exception as e:
                        st.error(str(e))
    
    with col2:
        st.markdown("### ⚔️ 执剑人裁决")
        
        if st.session_state.today_score is not None:
            # 评分显示
            score = st.session_state.today_score
            
            # 根据分数选择颜色
            if score >= 80:
                color = "#00ff88"
            elif score >= 60:
                color = "#00d4ff"
            elif score >= 40:
                color = "#ffaa00"
            else:
                color = "#ff4444"
            
            st.markdown(f"""
            <div class="metric-card">
                <div class="score-display" style="color: {color};">{score}</div>
                <p style="text-align: center; color: #666;">状态评分</p>
            </div>
            """, unsafe_allow_html=True)
            
            # 执剑人评语
            st.markdown(f"""
            <div class="swordholder-quote">
                "{st.session_state.today_comment}"
            </div>
            """, unsafe_allow_html=True)
            
            # 状态指示器
            if score >= 80:
                st.success("🌟 状态极佳 - 宇宙在你脚下")
            elif score >= 60:
                st.info("💫 状态良好 - 可以执行任务")
            elif score >= 40:
                st.warning("⚠️ 状态一般 - 注意休息")
            else:
                st.error("🚨 状态堪忧 - 立即停止内耗")
        else:
            st.info("💡 在左侧描述你的状态，接受执剑人的裁决")

# ============================================
# 模块三：历史仪表盘 (History Dashboard)
# ============================================
with tab3:
    st.markdown("## 📊 历史仪表盘 | History Dashboard")
    st.markdown("*监测熵增趋势，对抗时间的侵蚀*")
    
    # 加载历史数据
    df = load_from_csv()
    
    if not df.empty:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### 📈 状态评分趋势")
            
            # 使用 Plotly 绘制折线图
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=df['timestamp'],
                y=df['score'],
                mode='lines+markers',
                name='状态评分',
                line=dict(color='#00d4ff', width=3),
                marker=dict(size=10, symbol='diamond'),
                fill='tozeroy',
                fillcolor='rgba(0, 212, 255, 0.1)'
            ))
            
            # 添加平均线
            avg_score = df['score'].mean()
            fig.add_hline(
                y=avg_score,
                line_dash="dash",
                line_color="#ff6b6b",
                annotation_text=f"平均: {avg_score:.1f}",
                annotation_position="right"
            )
            
            fig.update_layout(
                template="plotly_dark",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis_title="时间",
                yaxis_title="评分",
                yaxis=dict(range=[0, 100]),
                height=400,
                margin=dict(l=20, r=20, t=40, b=20),
                font=dict(color='#888')
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### 📊 统计数据")
            
            # 统计指标
            st.metric("记录总数", len(df))
            st.metric("平均评分", f"{df['score'].mean():.1f}")
            st.metric("最高评分", f"{df['score'].max()}")
            st.metric("最低评分", f"{df['score'].min()}")
            
            # 评分分布
            st.markdown("### 📉 评分分布")
            
            # 分类统计
            excellent = len(df[df['score'] >= 80])
            good = len(df[(df['score'] >= 60) & (df['score'] < 80)])
            fair = len(df[(df['score'] >= 40) & (df['score'] < 60)])
            poor = len(df[df['score'] < 40])
            
            fig_pie = go.Figure(data=[go.Pie(
                labels=['极佳 (80+)', '良好 (60-79)', '一般 (40-59)', '堪忧 (<40)'],
                values=[excellent, good, fair, poor],
                hole=0.4,
                marker_colors=['#00ff88', '#00d4ff', '#ffaa00', '#ff4444']
            )])
            
            fig_pie.update_layout(
                template="plotly_dark",
                paper_bgcolor='rgba(0,0,0,0)',
                height=300,
                margin=dict(l=20, r=20, t=20, b=20),
                font=dict(color='#888'),
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=-0.2)
            )
            
            st.plotly_chart(fig_pie, use_container_width=True)
        
        # 历史记录表格
        st.markdown("### 📜 历史记录")
        
        # 显示最近的记录
        display_df = df.sort_values('timestamp', ascending=False).head(10)
        st.dataframe(
            display_df[['timestamp', 'score', 'comment']],
            use_container_width=True,
            hide_index=True,
            column_config={
                'timestamp': '时间',
                'score': st.column_config.ProgressColumn(
                    '评分',
                    min_value=0,
                    max_value=100,
                    format="%d"
                ),
                'comment': '执剑人评语'
            }
        )
        
        # 清空数据按钮
        with st.expander("⚠️ 危险操作"):
            if st.button("🗑️ 清空所有历史数据", type="secondary"):
                if os.path.exists(DATA_FILE):
                    os.remove(DATA_FILE)
                    st.success("数据已清空")
                    st.rerun()
    else:
        st.info("💡 暂无历史数据。在「状态监测」模块中记录你的第一次状态吧！")

# ============================================
# 页脚
# ============================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #444; padding: 20px;">
    <p>🌌 <strong>Wallfacer System</strong> | 执剑人系统 v1.0</p>
    <p style="font-size: 0.9em;">Powered by Google Gemini & Streamlit</p>
    <p style="font-size: 0.8em; font-style: italic;">"弱小和无知不是生存的障碍，傲慢才是。"</p>
</div>
""", unsafe_allow_html=True)
