@echo off
chcp 65001 >nul
color 0B
title 执剑人系统 - 时间压榨机器 v2.0

echo.
echo ███████████████████████████████████████████████████████████
echo ██                                                       ██
echo ██          🚀 执剑人系统 - 时间压榨机器 v2.0           ██
echo ██                                                       ██
echo ██          极限效率 • AI 驱动 • 数据驱动              ██
echo ██                                                       ██
echo ███████████████████████████████████████████████████████████
echo.

REM 检查 Python 是否安装
python --version >nul 2>&1
if errorlevel 1 (
    color 0C
    echo ❌ 错误: 未检测到 Python
    echo.
    echo 请先安装 Python: https://www.python.org/downloads/
    echo 安装时请勾选 "Add Python to PATH"
    echo.
    pause
    exit /b 1
)

REM 检查依赖
echo 📦 检查依赖...
pip list | findstr streamlit >nul 2>&1
if errorlevel 1 (
    color 0E
    echo ⚠️  首次运行，正在安装依赖...
    echo.
    pip install -r requirements.txt
    if errorlevel 1 (
        color 0C
        echo ❌ 依赖安装失败，请检查网络连接
        pause
        exit /b 1
    )
    echo.
    color 0B
)

REM 显示启动信息
echo ✅ 环境检查完毕
echo.
echo 🌐 应用将在以下地址启动:
echo.
echo    本地访问:  http://localhost:8501
echo.
echo    网络访问:  http://%COMPUTERNAME%:8501 或 http://本机IP:8501
echo.
echo ========================================================
echo.
echo 💡 提示:
echo    • 首次加载可能需要 5-10 秒
echo    • 关闭此窗口将停止应用
echo    • 访问应用后会自动在浏览器打开
echo.
echo ========================================================
echo.

REM 启动应用
color 0A
echo ⏱️  启动中... 请稍候
echo.
streamlit run app_v2.py --server.address 0.0.0.0 --server.port 8501

REM 错误处理
if errorlevel 1 (
    color 0C
    echo.
    echo ❌ 应用启动失败
    echo.
    echo 常见解决方案:
    echo   1. 检查 8501 端口是否被占用: netstat -ano ^| findstr 8501
    echo   2. 检查 app_v2.py 文件是否存在
    echo   3. 重新安装依赖: pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)
