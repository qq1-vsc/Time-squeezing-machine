@echo off
chcp 65001 >nul
color 0B
title 一键同步到 GitHub

echo.
echo ███████████████████████████████████████████████████████████
echo ██                                                       ██
echo ██         📤 一键同步到 GitHub                         ██
echo ██                                                       ██
echo ███████████████████████████████████████████████████████████
echo.

REM 检查 git 是否安装
git --version >nul 2>&1
if errorlevel 1 (
    color 0C
    echo ❌ 错误: 未检测到 Git
    echo.
    echo 请先安装 Git: https://git-scm.com/download/win
    echo.
    pause
    exit /b 1
)

REM 进入项目目录
cd /d "%~dp0"

echo ✅ 环境检查完毕
echo.

REM 显示当前状态
echo 📊 当前 Git 状态:
echo.
git status --short
echo.

REM 获取未提交的文件数
for /f %%i in ('git status --short ^| find /c /v ""') do set /a count=%%i

if %count% equ 0 (
    echo ✨ 没有需要同步的更改
    echo.
    timeout /t 2
    exit /b 0
)

echo ════════════════════════════════════════════════════════════
echo.
echo 📝 请输入提交信息 (默认: "更新: 代码和文档"):
set /p message=">>> "

if "%message%"=="" (
    set message=更新: 代码和文档
)

echo.
echo 🔄 正在同步...
echo.

REM 执行同步
git add .
if errorlevel 1 (
    color 0C
    echo ❌ 添加文件失败
    pause
    exit /b 1
)

git commit -m "%message%"
if errorlevel 1 (
    color 0C
    echo ❌ 提交失败
    pause
    exit /b 1
)

git push
if errorlevel 1 (
    color 0C
    echo ❌ 推送失败
    echo.
    echo 可能的原因:
    echo   1. 网络连接问题
    echo   2. GitHub 凭证过期
    echo   3. 远程仓库有冲突
    echo.
    echo 请运行以下命令手动解决:
    echo   git status
    echo   git push
    echo.
    pause
    exit /b 1
)

REM 成功
color 0A
echo.
echo ════════════════════════════════════════════════════════════
echo ✅ 同步成功！
echo.
echo 📚 GitHub 仓库: https://github.com/qq1-vsc/Time-squeezing-machine
echo.
echo ════════════════════════════════════════════════════════════
echo.
timeout /t 3
