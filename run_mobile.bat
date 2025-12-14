@echo off
echo ================================
echo   Wallfacer System 执剑人系统
echo   Mobile Access Mode (局域网模式)
echo ================================
echo.

REM Get local IP address
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4"') do (
    set IP=%%a
    goto :found
)
:found
set IP=%IP:~1%

echo Your local IP: %IP%
echo.
echo Access on mobile: http://%IP%:8501
echo.
echo Starting application...
echo.

streamlit run app.py --server.address 0.0.0.0 --server.port 8501

pause
