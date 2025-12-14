# -*- coding: utf-8 -*-
"""
执剑人系统 - 数据管理模块
处理任务数据的保存、加载和分析
"""

import sqlite3
import json
import pandas as pd
from datetime import datetime
import os

DB_FILE = "wallfacer_data.db"

def init_database():
    """初始化数据库"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # 创建计划表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS plans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            title TEXT,
            total_minutes INTEGER,
            tasks_json TEXT,
            status TEXT DEFAULT 'in_progress',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 创建任务执行记录表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS task_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            plan_id INTEGER,
            task_name TEXT NOT NULL,
            scheduled_minutes INTEGER,
            actual_minutes INTEGER,
            focus_level INTEGER,
            completed BOOLEAN DEFAULT 0,
            completed_at TIMESTAMP,
            notes TEXT,
            FOREIGN KEY (plan_id) REFERENCES plans(id)
        )
    ''')
    
    # 创建日志表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS daily_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL UNIQUE,
            total_scheduled_minutes INTEGER,
            total_actual_minutes INTEGER,
            completion_rate REAL,
            avg_focus_level REAL,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def save_plan(plan_data: dict, title: str = None) -> int:
    """保存计划到数据库"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    today = datetime.now().strftime("%Y-%m-%d")
    tasks_json = json.dumps(plan_data.get('tasks', []))
    
    cursor.execute('''
        INSERT INTO plans (date, title, total_minutes, tasks_json)
        VALUES (?, ?, ?, ?)
    ''', (today, title or "Daily Plan", plan_data.get('total_minutes', 0), tasks_json))
    
    conn.commit()
    plan_id = cursor.lastrowid
    conn.close()
    
    return plan_id

def save_task_record(plan_id: int, task_name: str, scheduled_min: int, 
                     actual_min: int, focus_level: int, completed: bool, notes: str = ""):
    """保存单个任务的执行记录"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    completed_at = datetime.now() if completed else None
    
    cursor.execute('''
        INSERT INTO task_records 
        (plan_id, task_name, scheduled_minutes, actual_minutes, focus_level, completed, completed_at, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (plan_id, task_name, scheduled_min, actual_min, focus_level, completed, completed_at, notes))
    
    conn.commit()
    conn.close()

def get_latest_plan():
    """获取最新的计划"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, date, total_minutes, tasks_json, status
        FROM plans
        ORDER BY created_at DESC
        LIMIT 1
    ''')
    
    result = cursor.fetchone()
    conn.close()
    
    if result:
        plan_id, date, total_minutes, tasks_json, status = result
        tasks = json.loads(tasks_json)
        return {
            'id': plan_id,
            'date': date,
            'total_minutes': total_minutes,
            'tasks': tasks,
            'status': status
        }
    return None

def get_today_plan():
    """获取今天的计划"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    today = datetime.now().strftime("%Y-%m-%d")
    
    cursor.execute('''
        SELECT id, date, total_minutes, tasks_json, status
        FROM plans
        WHERE date = ?
        ORDER BY created_at DESC
        LIMIT 1
    ''', (today,))
    
    result = cursor.fetchone()
    conn.close()
    
    if result:
        plan_id, date, total_minutes, tasks_json, status = result
        tasks = json.loads(tasks_json)
        return {
            'id': plan_id,
            'date': date,
            'total_minutes': total_minutes,
            'tasks': tasks,
            'status': status
        }
    return None

def get_all_plans(limit: int = 30):
    """获取所有计划"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, date, total_minutes, status, created_at
        FROM plans
        ORDER BY created_at DESC
        LIMIT ?
    ''', (limit,))
    
    results = cursor.fetchall()
    conn.close()
    
    plans = []
    for plan_id, date, total_minutes, status, created_at in results:
        plans.append({
            'id': plan_id,
            'date': date,
            'total_minutes': total_minutes,
            'status': status,
            'created_at': created_at
        })
    
    return plans

def get_plan_records(plan_id: int):
    """获取计划的所有任务记录"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT task_name, scheduled_minutes, actual_minutes, focus_level, completed, notes
        FROM task_records
        WHERE plan_id = ?
        ORDER BY id ASC
    ''', (plan_id,))
    
    results = cursor.fetchall()
    conn.close()
    
    records = []
    for task_name, scheduled_min, actual_min, focus_level, completed, notes in results:
        records.append({
            'task_name': task_name,
            'scheduled_minutes': scheduled_min,
            'actual_minutes': actual_min,
            'focus_level': focus_level,
            'completed': completed,
            'notes': notes
        })
    
    return records

def update_plan_status(plan_id: int, status: str):
    """更新计划状态"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE plans
        SET status = ?
        WHERE id = ?
    ''', (status, plan_id))
    
    conn.commit()
    conn.close()

def get_statistics():
    """获取统计数据"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # 获取最近 30 天的数据
    cursor.execute('''
        SELECT 
            date,
            SUM(scheduled_minutes) as scheduled,
            SUM(actual_minutes) as actual,
            AVG(focus_level) as avg_focus,
            COUNT(*) as task_count,
            SUM(CASE WHEN completed = 1 THEN 1 ELSE 0 END) as completed_count
        FROM task_records tr
        JOIN plans p ON tr.plan_id = p.id
        WHERE date >= date('now', '-30 days')
        GROUP BY date
        ORDER BY date DESC
    ''')
    
    results = cursor.fetchall()
    conn.close()
    
    data = []
    for date, scheduled, actual, avg_focus, task_count, completed_count in results:
        data.append({
            'date': date,
            'scheduled_minutes': scheduled or 0,
            'actual_minutes': actual or 0,
            'avg_focus_level': avg_focus or 0,
            'task_count': task_count,
            'completion_rate': (completed_count / task_count * 100) if task_count > 0 else 0
        })
    
    return data

def export_to_csv(filename: str = None):
    """导出数据为 CSV"""
    stats = get_statistics()
    df = pd.DataFrame(stats)
    
    if filename is None:
        filename = f"wallfacer_stats_{datetime.now().strftime('%Y%m%d')}.csv"
    
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    return filename

# 初始化数据库
init_database()
