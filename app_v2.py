# -*- coding: utf-8 -*-
"""
Wallfacer System v2.0 (执剑人系统 - 疯狂时间压榨机器)
极致效率的学习管理工具
"""

import streamlit as st
from openai import OpenAI
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import json
import os
from datetime import datetime, timedelta
import time
import math
from data_manager import (
    init_database, save_plan, save_task_record, get_latest_plan,
    get_today_plan, get_all_plans, get_plan_records, update_plan_status,
    get_statistics, export_to_csv
)

# ============================================
# 页面配置
# ============================================
st.set_page_config(
    page_title="时间压榨机器 | 执剑人系统 v2.0",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# 极限风格 CSS
# ============================================
st.markdown("""
<style>
    /* 黑暗高强度主题 */
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a0a2e 50%, #0a0a1a 100%);
        color: #00ff88;
    }
    
    h1, h2, h3 {
        color: #00ff88 !important;
        font-family: 'Courier New', monospace;
        text-shadow: 0 0 20px rgba(0, 255, 136, 0.5);
        font-weight: 900;
    }
    
    /* 极限倒计时样式 */
    .timer-display {
        font-size: 120px;
        font-weight: 900;
        text-align: center;
        font-family: 'Courier New', monospace;
        text-shadow: 0 0 40px rgba(0, 255, 136, 0.8);
        animation: pulse 0.8s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    /* 警告阶段 */
    .timer-warning {
        color: #ffaa00 !important;
        text-shadow: 0 0 40px rgba(255, 170, 0, 0.8);
    }
    
    /* 危急阶段 */
    .timer-danger {
        color: #ff4444 !important;
        text-shadow: 0 0 40px rgba(255, 68, 68, 0.8);
        animation: blink 0.4s infinite;
    }
    
    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.3; }
    }
    
    /* 任务卡片 */
    .task-card {
        background: linear-gradient(145deg, #1a1a3e, #2a1050);
        border: 2px solid #00ff88;
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 0 30px rgba(0, 255, 136, 0.3), inset 0 0 20px rgba(0, 255, 136, 0.1);
        transition: all 0.3s ease;
    }
    
    .task-card:hover {
        box-shadow: 0 0 50px rgba(0, 255, 136, 0.5), inset 0 0 30px rgba(0, 255, 136, 0.2);
        border-color: #00ffff;
    }
    
    .task-active {
        background: linear-gradient(145deg, #2a2a5e, #3a2070);
        border-color: #00ffff;
        box-shadow: 0 0 60px rgba(0, 255, 255, 0.4);
    }
    
    /* 按钮 */
    .stButton > button {
        background: linear-gradient(90deg, #00ff88, #00ffaa);
        color: #000000;
        border: none;
        font-weight: 900;
        font-size: 16px;
        padding: 15px 30px;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(90deg, #00ffaa, #00ffcc);
        box-shadow: 0 0 30px rgba(0, 255, 136, 0.6);
        transform: scale(1.05);
    }
    
    /* 进度条 */
    .stProgress > div > div {
        background: linear-gradient(90deg, #00ff88, #00ffff);
        box-shadow: 0 0 20px rgba(0, 255, 136, 0.5);
    }
    
    /* 指标 */
    .metric-extreme {
        background: linear-gradient(145deg, #1a1a3e, #2a1050);
        border: 2px solid #00ff88;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 0 30px rgba(0, 255, 136, 0.3);
    }
    
    .metric-value {
        font-size: 48px;
        font-weight: 900;
        color: #00ff88;
        text-shadow: 0 0 20px rgba(0, 255, 136, 0.6);
    }
    
    .metric-label {
        font-size: 14px;
        color: #888;
        margin-top: 5px;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# 初始化数据库和 Session State
# ============================================
init_database()

def init_session_state():
    if 'client' not in st.session_state:
        st.session_state.client = None
    if 'api_configured' not in st.session_state:
        st.session_state.api_configured = False
    if 'api_key' not in st.session_state:
        st.session_state.api_key = ""
    if 'plan' not in st.session_state:
        st.session_state.plan = ""
    if 'optimized_plan' not in st.session_state:
        st.session_state.optimized_plan = []
    if 'executing' not in st.session_state:
        st.session_state.executing = False
    if 'current_task_idx' not in st.session_state:
        st.session_state.current_task_idx = 0
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'start_time' not in st.session_state:
        st.session_state.start_time = None
    if 'total_seconds' not in st.session_state:
        st.session_state.total_seconds = 0
    if 'plan_data' not in st.session_state:
        st.session_state.plan_data = None
    if 'current_plan_id' not in st.session_state:
        st.session_state.current_plan_id = None

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
        st.error(f"❌ API 配置失败: {str(e)}")
        st.session_state.api_configured = False
        return False

def call_deepseek(messages: list, temperature=0.7) -> str:
    """调用 DeepSeek API"""
    if not st.session_state.api_configured:
        raise Exception("API 未配置")
    
    try:
        response = st.session_state.client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            temperature=temperature,
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        raise Exception(f"API 调用失败: {str(e)}")

# ============================================
# 核心功能：激进的计划优化
# ============================================
def optimize_plan_aggressive(user_plan: str) -> dict:
    """
    激进优化计划 - 极限压榨时间
    """
    system_prompt = """你是一个极端的时间优化大师,代号'时间杀手'。你的目标是将用户的计划疯狂优化,让他们的每一秒都用于学习和成长。

你必须:
1. 将计划分解成具体的微任务(不超过25分钟)
2. 对每个任务设定激进的时间限制(边界压力)
3. 标注任务优先级和学习价值
4. 消除所有浪费(休息时间最小化)
5. 最大化深度工作时间

返回格式(纯JSON，无其他内容):
{
  "total_minutes": 总时长,
  "tasks": [
    {
      "id": 任务序号,
      "name": "任务名称",
      "minutes": 预估分钟数,
      "priority": "S/A/B",
      "focus": "专注度(1-10)",
      "method": "推荐方法或提示",
      "warning": "时间压力提示"
    }
  ],
  "motivation": "激励语句(刘慈欣风格,冷酷而振奋)",
  "tips": "极限执行建议"
}"""
    
    try:
        response = call_deepseek(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"我的今日计划: {user_plan}\n\n请激进优化，让我达到极限效率！"}
            ],
            temperature=0.8
        )
        
        # 清理 JSON 响应
        cleaned = response.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.split("\n", 1)[1]
        if cleaned.endswith("```"):
            cleaned = cleaned.rsplit("```", 1)[0]
        cleaned = cleaned.strip()
        
        plan_data = json.loads(cleaned)
        return plan_data
    except Exception as e:
        raise Exception(f"计划优化失败: {str(e)}")

def get_task_suggestion(task: dict, elapsed_seconds: int, total_seconds: int) -> str:
    """
    实时任务建议 - AI 根据进度给出指导
    """
    progress = elapsed_seconds / total_seconds if total_seconds > 0 else 0
    
    system_prompt = f"""你是一个极端激励的时间教练。用户正在执行一个高强度学习计划。

当前进度: {progress*100:.0f}%
已用时间: {elapsed_seconds//60}分{elapsed_seconds%60}秒
当前任务: {task['name']}
剩余时间: {task['minutes']}分钟
专注度要求: {task['focus']}/10

根据进度给出实时激励和建议。语言要冷酷、直接、充满压力感(参考刘慈欣)。"""
    
    try:
        response = call_deepseek(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": "给我一句激励语和建议"}
            ],
            temperature=0.6
        )
        return response
    except:
        return "继续推进，时间在流逝。"

# ============================================
# 侧边栏 - API 配置 + 数据管理
# ============================================
with st.sidebar:
    st.markdown("## ⚡ 时间压榨机器")
    st.markdown("疯狂优化 | 极限效率 | 全力学习")
    st.markdown("---")
    
    st.markdown("### 🔌 API 配置")
    
    api_key_input = st.text_input(
        "DeepSeek API Key",
        type="password",
        value=st.session_state.api_key,
        help="从 platform.deepseek.com 获取"
    )
    
    if st.button("🚀 启动系统", use_container_width=True):
        if api_key_input:
            with st.spinner("系统启动中..."):
                if configure_deepseek(api_key_input):
                    st.success("✅ 系统就绪！")
                else:
                    st.error("❌ 启动失败")
        else:
            st.warning("请输入 API Key")
    
    if st.session_state.api_configured:
        st.markdown("🟢 **系统: 激活**")
    else:
        st.markdown("🔴 **系统: 待激活**")
    
    st.markdown("---")
    st.markdown("### 📚 计划管理")
    
    # 继续上一次
    latest_plan = get_latest_plan()
    if latest_plan:
        st.markdown(f"**上次计划:** {latest_plan['date']}")
        if st.button("▶️ 继续上一次", use_container_width=True):
            st.session_state.plan_data = latest_plan
            st.session_state.optimized_plan = latest_plan['tasks']
            st.session_state.current_plan_id = latest_plan['id']
            st.session_state.executing = False
            st.rerun()
    
    # 继续今天的
    today_plan = get_today_plan()
    if today_plan and today_plan != latest_plan:
        st.markdown(f"**今天计划:** {today_plan['date']}")
        if st.button("▶️ 继续今天", use_container_width=True):
            st.session_state.plan_data = today_plan
            st.session_state.optimized_plan = today_plan['tasks']
            st.session_state.current_plan_id = today_plan['id']
            st.session_state.executing = False
            st.rerun()
    
    st.markdown("---")
    st.markdown("### 💡 使用说明")
    st.markdown("""
    1. 输入今日计划
    2. 点击"疯狂优化"
    3. 确认计划
    4. 开始执行
    5. 实时对话调整
    6. 所有数据自动保存
    """)

# ============================================
# 主页面
# ============================================
st.markdown("""
<div style="text-align: center; margin: 30px 0;">
    <h1 style="font-size: 3em; margin: 0;">⚡ 时间压榨机器</h1>
    <p style="color: #00ff88; font-size: 1.3em; margin: 5px;">执剑人系统 v2.0 | 极限效率工具</p>
    <p style="color: #888; font-size: 0.9em;">"每一秒都用于成长，没有任何浪费"</p>
</div>
""", unsafe_allow_html=True)

# ============================================
# Tab 分区
# ============================================
tab1, tab2, tab3 = st.tabs(["🎯 计划优化", "⏱️ 实时执行", "📊 数据面板"])

# ============================================
# Tab 1: 计划优化
# ============================================
with tab1:
    st.markdown("## 📝 输入你的疯狂计划")
    st.markdown("*系统将进行激进优化，消除所有浪费*")
    
    user_plan = st.text_area(
        "描述你今天要完成的所有事项",
        height=200,
        placeholder="例如：学习深度学习第5章、完成3个LeetCode题目、复习线性代数、阅读论文2篇...",
        key="plan_input"
    )
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("🔥 疯狂优化", use_container_width=True, type="primary"):
            if not st.session_state.api_configured:
                st.error("❌ 请先在侧边栏启动系统")
            elif not user_plan.strip():
                st.warning("⚠️ 请输入计划")
            else:
                with st.spinner("AI正在疯狂优化你的计划..."):
                    try:
                        plan_data = optimize_plan_aggressive(user_plan)
                        st.session_state.optimized_plan = plan_data['tasks']
                        st.session_state.plan_data = plan_data
                        st.session_state.plan = user_plan
                        st.success("✅ 计划优化完成！")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ 优化失败: {str(e)}")
    
    with col2:
        if st.button("🔄 清空计划", use_container_width=True):
            st.session_state.optimized_plan = []
            st.session_state.plan_data = None
            st.rerun()
    
    # 显示优化结果
    if st.session_state.plan_data:
        st.markdown("---")
        st.markdown("## 📊 优化方案")
        
        plan_data = st.session_state.plan_data
        
        # 显示统计信息
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-extreme">
                <div class="metric-value">{plan_data['total_minutes']}</div>
                <div class="metric-label">总分钟数</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-extreme">
                <div class="metric-value">{len(plan_data['tasks'])}</div>
                <div class="metric-label">任务数</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            s_count = sum(1 for t in plan_data['tasks'] if t['priority'] == 'S')
            st.markdown(f"""
            <div class="metric-extreme">
                <div class="metric-value">{s_count}</div>
                <div class="metric-label">核心任务(S)</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            avg_focus = sum(int(t['focus']) for t in plan_data['tasks']) / len(plan_data['tasks'])
            st.markdown(f"""
            <div class="metric-extreme">
                <div class="metric-value">{avg_focus:.1f}</div>
                <div class="metric-label">平均专注度</div>
            </div>
            """, unsafe_allow_html=True)
        
        # 显示激励语
        st.markdown(f"""
        <div style="background: linear-gradient(145deg, #1a1a3e, #2a1050); 
                    border: 2px solid #00ff88; border-radius: 15px; padding: 20px; 
                    margin: 20px 0; text-align: center;">
            <p style="color: #00ff88; font-size: 1.2em; font-style: italic;">
                "{plan_data['motivation']}"
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # 显示任务列表
        st.markdown("## 📋 任务明细")
        
        for task in plan_data['tasks']:
            priority_colors = {"S": "🔴", "A": "🟠", "B": "🟡"}
            priority_emoji = priority_colors.get(task['priority'], "⚪")
            
            st.markdown(f"""
            <div class="task-card">
                <div style="display: flex; justify-content: space-between; align-items: start;">
                    <div style="flex: 1;">
                        <h3 style="margin: 0; color: #00ff88;">
                            {priority_emoji} {task['name']}
                        </h3>
                        <p style="color: #888; margin: 5px 0; font-size: 0.9em;">
                            ⏱️ {task['minutes']}分 | 💪 专注度: {task['focus']}/10
                        </p>
                        <p style="color: #00ffaa; margin: 10px 0; font-size: 0.95em;">
                            📍 {task['method']}
                        </p>
                        <p style="color: #ffaa00; margin: 0; font-size: 0.85em;">
                            ⚠️ {task['warning']}
                        </p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        if st.button("▶️ 开始执行计划", use_container_width=True, type="primary"):
            # 保存计划到数据库
            plan_id = save_plan(plan_data, title=f"Daily Plan {datetime.now().strftime('%Y-%m-%d %H:%M')}")
            st.session_state.current_plan_id = plan_id
            st.session_state.executing = True
            st.session_state.current_task_idx = 0
            st.session_state.start_time = time.time()
            st.session_state.total_seconds = plan_data['total_minutes'] * 60
            st.session_state.chat_history = []
            st.rerun()

# ============================================
# Tab 2: 实时执行
# ============================================
with tab2:
    if not st.session_state.executing:
        st.info("💡 请先在「计划优化」中完成计划优化和启动")
    else:
        st.markdown("## ⏱️ 实时执行模式")
        
        plan_data = st.session_state.plan_data
        tasks = plan_data['tasks']
        current_idx = st.session_state.current_task_idx
        
        if current_idx < len(tasks):
            current_task = tasks[current_idx]
            elapsed = time.time() - st.session_state.start_time
            elapsed_seconds = int(elapsed)
            
            # 计算当前任务的剩余时间
            task_start_seconds = sum(t['minutes'] * 60 for t in tasks[:current_idx])
            task_elapsed = elapsed_seconds - task_start_seconds
            task_remaining = max(0, current_task['minutes'] * 60 - task_elapsed)
            task_progress = 1.0 - (task_remaining / (current_task['minutes'] * 60)) if current_task['minutes'] > 0 else 0
            
            # 总体进度
            total_progress = elapsed_seconds / st.session_state.total_seconds
            
            # ============================================
            # 计时器显示（根据阶段改变风格）
            # ============================================
            col1, col2 = st.columns([2, 1])
            
            with col1:
                minutes = task_remaining // 60
                seconds = task_remaining % 60
                
                # 根据剩余时间选择样式
                if task_remaining > current_task['minutes'] * 60 * 0.5:
                    timer_class = "timer-display"
                elif task_remaining > current_task['minutes'] * 60 * 0.2:
                    timer_class = "timer-display timer-warning"
                else:
                    timer_class = "timer-display timer-danger"
                
                st.markdown(f"""
                <div class="{timer_class}">
                    {minutes:02d}:{seconds:02d}
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-extreme">
                    <div class="metric-value">{current_idx + 1}/{len(tasks)}</div>
                    <div class="metric-label">当前任务</div>
                </div>
                """, unsafe_allow_html=True)
            
            # ============================================
            # 当前任务详情
            # ============================================
            st.markdown("---")
            st.markdown(f"""
            <div class="task-card task-active">
                <h2 style="margin: 0; color: #00ffff;">{current_task['name']}</h2>
                <p style="color: #00ff88; font-size: 1.1em; margin: 10px 0;">
                    💪 专注度要求: {current_task['focus']}/10
                </p>
                <p style="color: #00ffaa; font-size: 1em; margin: 10px 0;">
                    📍 {current_task['method']}
                </p>
                <p style="color: #ffaa00; font-size: 0.95em; margin: 10px 0;">
                    ⚠️ {current_task['warning']}
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # ============================================
            # 当前任务进度条
            # ============================================
            st.markdown("### ⏱️ 当前任务进度")
            st.progress(min(task_progress, 1.0))
            st.caption(f"已用: {int(task_elapsed // 60)}m {int(task_elapsed % 60)}s / 总计: {current_task['minutes']}m")
            
            # ============================================
            # 总体进度条
            # ============================================
            st.markdown("### 📊 全天总进度")
            st.progress(min(total_progress, 1.0))
            
            hours = int(elapsed_seconds // 3600)
            mins = int((elapsed_seconds % 3600) // 60)
            secs = int(elapsed_seconds % 60)
            st.caption(f"已用时: {hours}h {mins}m {secs}s / 总计: {plan_data['total_minutes']}min")
            
            # ============================================
            # 剩余任务预览（不混杂，分块显示）
            # ============================================
            if current_idx < len(tasks) - 1:
                st.markdown("---")
                st.markdown("### 📋 接下来的任务")
                
                # 只显示接下来的 3 个任务
                for i in range(current_idx + 1, min(current_idx + 4, len(tasks))):
                    task = tasks[i]
                    st.markdown(f"""
                    <div style="background: rgba(0, 255, 136, 0.05); border-left: 3px solid #00ff88; 
                                padding: 10px 15px; margin: 10px 0; border-radius: 5px;">
                        <p style="color: #888; margin: 0; font-size: 0.9em;">任务 {i+1}</p>
                        <p style="color: #00ff88; margin: 5px 0; font-weight: bold;">{task['name']}</p>
                        <p style="color: #666; margin: 0; font-size: 0.85em;">⏱️ {task['minutes']}分 | 💪 {task['focus']}/10</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            # ============================================
            # 任务导航
            # ============================================
            st.markdown("---")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if current_idx > 0 and st.button("⏮️ 上一个任务"):
                    st.session_state.current_task_idx -= 1
                    st.rerun()
            
            with col2:
                if st.button("✅ 完成当前任务"):
                    # 保存任务记录
                    if st.session_state.current_plan_id:
                        save_task_record(
                            plan_id=st.session_state.current_plan_id,
                            task_name=current_task['name'],
                            scheduled_min=current_task['minutes'],
                            actual_min=int(task_elapsed // 60),
                            focus_level=current_task['focus'],
                            completed=True
                        )
                    
                    if current_idx < len(tasks) - 1:
                        st.session_state.current_task_idx += 1
                        st.info(f"✅ 任务完成！进入下一个任务")
                    else:
                        # 标记计划完成
                        if st.session_state.current_plan_id:
                            update_plan_status(st.session_state.current_plan_id, 'completed')
                        st.session_state.executing = False
                        st.success(f"🎉 所有任务完成！总耗时: {int(elapsed_seconds // 60)} 分钟")
                    st.rerun()
            
            with col3:
                if st.button("⏹️ 停止执行"):
                    st.session_state.executing = False
                    st.rerun()
            
            # ============================================
            # AI 对话区（实时调整方案）
            # ============================================
            st.markdown("---")
            st.markdown("## 💬 实时对话（调整方案）")
            
            user_message = st.text_input(
                "与AI讨论(修改方案、获取帮助、寻求激励)",
                placeholder="例如：这个任务太难了，能降低难度吗？ | 给我一些激励 | 跳过这个任务",
                key="user_message"
            )
            
            if user_message:
                # 添加用户消息到历史
                st.session_state.chat_history.append({
                    "role": "user",
                    "content": user_message
                })
                
                # 调用 AI
                try:
                    system_prompt = f"""你是一个激进的时间教练和学习顾问。
当前任务: {current_task['name']}
已用时间: {elapsed_seconds//60}分{elapsed_seconds%60}秒
剩余时间: {task_remaining//60}分{task_remaining%60}秒
专注度要求: {current_task['focus']}/10

用户的要求: {user_message}

请以激励、冷酷但实用的风格回应。如果用户要求调整，给出具体方案。"""
                    
                    response = call_deepseek(
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_message}
                        ],
                        temperature=0.7
                    )
                    
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": response
                    })
                    
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ AI 响应失败: {str(e)}")
            
            # 显示对话历史
            if st.session_state.chat_history:
                st.markdown("### 📝 对话历史")
                for msg in st.session_state.chat_history:
                    if msg["role"] == "user":
                        st.markdown(f"**你:** {msg['content']}")
                    else:
                        st.markdown(f"**AI:** {msg['content']}")
        else:
            st.success("🎉 所有任务完成！")
            if st.button("🔄 返回计划页面"):
                st.session_state.executing = False
                st.rerun()

# ============================================
# Tab 3: 数据面板
# ============================================
with tab3:
    st.markdown("## 📊 数据分析面板")
    
    # 创建子 Tab
    tab3_1, tab3_2, tab3_3 = st.tabs(["📈 今日统计", "📊 历史趋势", "📚 所有计划"])
    
    with tab3_1:
        if st.session_state.plan_data:
            plan_data = st.session_state.plan_data
            tasks = plan_data['tasks']
            
            # 任务优先级分布
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown("### 优先级分布")
                priority_counts = {}
                for task in tasks:
                    p = task['priority']
                    priority_counts[p] = priority_counts.get(p, 0) + 1
                
                fig = go.Figure(data=[go.Pie(
                    labels=list(priority_counts.keys()),
                    values=list(priority_counts.values()),
                    hole=0.3,
                    marker=dict(colors=['#ff4444', '#ffaa00', '#00ff88'])
                )])
                fig.update_layout(
                    template="plotly_dark",
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#00ff88'),
                    height=350
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("### 时间分布")
                times = [t['minutes'] for t in tasks]
                names = [t['name'][:15] for t in tasks]
                
                fig = go.Figure(data=[go.Bar(
                    y=names,
                    x=times,
                    orientation='h',
                    marker=dict(color=times, colorscale='Plasma')
                )])
                fig.update_layout(
                    template="plotly_dark",
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#00ff88'),
                    height=350,
                    xaxis_title="分钟",
                    yaxis_title=""
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # 详细统计
            st.markdown("---")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                avg_time = sum(t['minutes'] for t in tasks) / len(tasks)
                st.metric("平均任务时长", f"{avg_time:.0f}min")
            
            with col2:
                avg_focus = sum(int(t['focus']) for t in tasks) / len(tasks)
                st.metric("平均专注度", f"{avg_focus:.1f}/10")
            
            with col3:
                s_tasks = len([t for t in tasks if t['priority'] == 'S'])
                st.metric("核心任务数", s_tasks)
            
            with col4:
                total_time = sum(t['minutes'] for t in tasks)
                st.metric("总投入时间", f"{total_time}min")
        else:
            st.info("💡 暂无计划数据")
    
    with tab3_2:
        st.markdown("### 📊 30天历史趋势")
        
        stats = get_statistics()
        if stats:
            df = pd.DataFrame(stats)
            
            # 时间趋势
            fig_time = go.Figure()
            fig_time.add_trace(go.Scatter(
                x=df['date'],
                y=df['scheduled_minutes'],
                name='计划时间',
                line=dict(color='#00ff88', width=3)
            ))
            fig_time.add_trace(go.Scatter(
                x=df['date'],
                y=df['actual_minutes'],
                name='实际时间',
                line=dict(color='#00ffaa', width=3, dash='dash')
            ))
            fig_time.update_layout(
                template="plotly_dark",
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#00ff88'),
                height=400,
                xaxis_title="日期",
                yaxis_title="分钟",
                hovermode='x unified'
            )
            st.plotly_chart(fig_time, use_container_width=True)
            
            # 专注度趋势
            fig_focus = go.Figure()
            fig_focus.add_trace(go.Scatter(
                x=df['date'],
                y=df['avg_focus_level'],
                name='平均专注度',
                mode='lines+markers',
                line=dict(color='#ffaa00', width=3),
                marker=dict(size=8)
            ))
            fig_focus.update_layout(
                template="plotly_dark",
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#00ff88'),
                height=400,
                xaxis_title="日期",
                yaxis_title="专注度 (1-10)",
                hovermode='x'
            )
            st.plotly_chart(fig_focus, use_container_width=True)
            
            # 完成率
            fig_completion = go.Figure()
            fig_completion.add_trace(go.Scatter(
                x=df['date'],
                y=df['completion_rate'],
                name='完成率',
                mode='lines+markers',
                line=dict(color='#00ffff', width=3),
                marker=dict(size=8),
                fill='tozeroy',
                fillcolor='rgba(0, 255, 255, 0.2)'
            ))
            fig_completion.update_layout(
                template="plotly_dark",
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#00ff88'),
                height=400,
                xaxis_title="日期",
                yaxis_title="完成率 (%)",
                hovermode='x'
            )
            st.plotly_chart(fig_completion, use_container_width=True)
            
            # 统计汇总
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                avg_planned = df['scheduled_minutes'].mean()
                st.metric("平均计划时间", f"{avg_planned:.0f}min")
            with col2:
                avg_actual = df['actual_minutes'].mean()
                st.metric("平均实际时间", f"{avg_actual:.0f}min")
            with col3:
                avg_focus = df['avg_focus_level'].mean()
                st.metric("平均专注度", f"{avg_focus:.1f}/10")
            with col4:
                avg_completion = df['completion_rate'].mean()
                st.metric("平均完成率", f"{avg_completion:.1f}%")
        else:
            st.info("💡 暂无历史数据")
    
    with tab3_3:
        st.markdown("### 📚 所有计划记录")
        
        all_plans = get_all_plans(limit=50)
        if all_plans:
            # 创建数据表
            plans_data = []
            for plan in all_plans:
                records = get_plan_records(plan['id'])
                completed = sum(1 for r in records if r['completed'])
                total = len(records)
                
                plans_data.append({
                    '日期': plan['date'],
                    '状态': plan['status'],
                    '任务数': total,
                    '完成数': completed,
                    '完成率': f"{(completed/total*100):.0f}%" if total > 0 else "0%",
                    '创建时间': plan['created_at']
                })
            
            df_plans = pd.DataFrame(plans_data)
            st.dataframe(df_plans, use_container_width=True, hide_index=True)
            
            # 导出功能
            if st.button("📥 导出数据为 CSV"):
                filename = export_to_csv()
                with open(filename, 'rb') as f:
                    st.download_button(
                        label="下载 CSV 文件",
                        data=f.read(),
                        file_name=filename,
                        mime="text/csv"
                    )
        else:
            st.info("💡 暂无计划记录")

# ============================================
# 页脚
# ============================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #444; padding: 20px;">
    <p>⚡ <strong>时间压榨机器 v2.0</strong> | 疯狂优化 · 极限效率</p>
    <p style="font-size: 0.9em; color: #666;">
        "不要浪费每一秒，每一秒都是成长的机会"
    </p>
</div>
""", unsafe_allow_html=True)
