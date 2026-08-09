@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo.
echo  ╔══════════════════════════════╗
echo  ║     daily-code · 每日推送    ║
echo  ╚══════════════════════════════╝
echo.

:: 获取今天的日期
for /f "tokens=2 delims==" %%I in ('wmic os get localdatetime /value') do set datetime=%%I
set today=%datetime:~0,4%-%datetime:~4,2%-%datetime:~6,2%

echo  📅 日期: %today%
echo  📝 正在提交...

git add -A
git commit -m "%today% · 每日学习打卡" 2>nul

if %errorlevel% neq 0 (
    echo  ⚠ 没有新内容需要提交（今天还没写？）
    echo.
    pause
    exit /b 0
)

echo  🚀 正在推送到 GitHub...
git push

if %errorlevel% neq 0 (
    echo.
    echo  ❌ 推送失败！请检查网络或 GitHub 配置。
    echo.
    pause
    exit /b 1
)

echo.
echo  ✅ 打卡成功！今天又进了一步。
echo  🔗 去 github.com 看看你的绿点吧
echo.
pause
