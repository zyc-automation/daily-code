@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo.
echo ============================================
echo    daily-code 打卡推送
echo ============================================
echo.

for /f "usebackq delims=" %%i in (`powershell -NoProfile -Command "Get-Date -Format yyyy-MM-dd"`) do set today=%%i

echo    日期: %today%
echo.

git add -A
git commit -m "%today% daily check-in" >nul 2>&1
if errorlevel 1 (
    echo    [提示] 没有改动可提交，请先保存你的代码/笔记
    echo.
    pause
    exit /b 0
)

echo    正在推送到 GitHub ...
git push
if errorlevel 1 (
    echo.
    echo    [失败] 推送失败，多半是网络问题，稍后重试即可
    echo.
    pause
    exit /b 1
)

echo.
echo ============================================
echo    完成！绿点已更新
echo    github.com/zyc-automation
echo ============================================
echo.
pause
