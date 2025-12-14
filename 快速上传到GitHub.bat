@echo off
REM 执剑人系统 v2.0 - GitHub 快速上传脚本

cd /d "%~dp0"

echo.
echo ======================================
echo   执剑人系统 v2.0
echo   GitHub 快速上传工具
echo ======================================
echo.

REM 检查是否已初始化 Git
if not exist .git (
    echo [*] 初始化 Git 仓库...
    git init
    
    echo [*] 配置全局用户信息...
    git config --global user.name "Wallfacer System User"
    git config --global user.email "user@example.com"
    
    echo [*] 创建 .gitignore...
    (
        echo __pycache__/
        echo *.pyc
        echo .streamlit/secrets.toml
        echo wallfacer_data.db
        echo *.csv
        echo .env
        echo .venv/
        echo venv/
    ) > .gitignore
    
    echo [*] 首次提交...
    git add .
    git commit -m "初始化: 执剑人系统 v2.0 - 时间压榨机器"
    
    echo.
    echo ======================================
    echo   Git 初始化完成！
    echo ======================================
    echo.
    echo 下一步:
    echo 1. 在 GitHub 创建新仓库
    echo 2. 复制仓库 HTTPS 链接
    echo 3. 运行下面的命令:
    echo.
    echo   git remote add origin https://github.com/你的用户名/wallfacer-system.git
    echo   git branch -M main
    echo   git push -u origin main
    echo.
) else (
    echo [✓] Git 仓库已初始化
    echo.
    echo [*] 检查文件变更...
    git status
    
    echo.
    set /p commit_msg="输入提交信息 (Commit Message): "
    
    if "%commit_msg%"=="" (
        echo [!] 提交信息不能为空
        pause
        exit /b 1
    )
    
    echo [*] 添加所有文件...
    git add .
    
    echo [*] 提交更改...
    git commit -m "%commit_msg%"
    
    echo [*] 推送到远程...
    git push
    
    if %errorlevel% equ 0 (
        echo.
        echo ======================================
        echo   ✓ 推送成功！
        echo ======================================
    ) else (
        echo.
        echo ======================================
        echo   ! 推送失败，请检查远程配置
        echo ======================================
    )
)

pause
