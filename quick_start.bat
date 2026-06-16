@echo off
chcp 65001 >nul
echo ========================================
echo   DeepShield v2.0 一键启动脚本
echo ========================================
echo.

REM 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [×] Python 未安装或未添加到 PATH
    pause
    exit /b 1
)
echo [√] Python 环境正常

REM 检查 Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo [×] Node.js 未安装或未添加到 PATH
    pause
    exit /b 1
)
echo [√] Node.js 环境正常
echo.

REM 创建必要目录
echo [1/4] 创建必要目录...
if not exist "uploads" mkdir uploads
if not exist "reports" mkdir reports
if not exist "logs" mkdir logs
if not exist "evidence" mkdir evidence
echo [√] 目录结构就绪
echo.

REM 启动后端
echo [2/4] 启动后端服务...
start "DeepShield Backend" cmd /k "cd /d %~dp0 && python app.py"
timeout /t 3 /nobreak >nul
echo [√] 后端服务已启动 (Port 5001)
echo.

REM 启动前端
echo [3/4] 启动前端服务...
start "DeepShield Frontend" cmd /k "cd /d %~dp0frontend && npm run dev"
timeout /t 5 /nobreak >nul
echo [√] 前端服务已启动 (Port 5473)
echo.

REM 打开浏览器
echo [4/4] 正在打开浏览器...
timeout /t 2 /nobreak >nul
start http://localhost:5473
echo [√] 浏览器已打开
echo.

echo ========================================
echo   DeepShield 已成功启动！
echo ========================================
echo.
echo 访问地址：
echo   - 前端: http://localhost:5473
echo   - 后端: http://localhost:5001/api/health
echo.
echo LAN 访问：
echo   - 前端: http://[你的IP]:5473
echo   - 后端: http://[你的IP]:5001
echo.
echo 提示：
echo   - 请勿关闭弹出的命令行窗口
echo   - 按 Ctrl+C 可停止服务
echo   - 查看 UPGRADE_REPORT.md 了解新功能
echo.
pause
