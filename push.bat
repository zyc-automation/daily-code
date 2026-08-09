@echo off
cd /d "%~dp0"

echo.
echo ============================================
echo   daily-code - Push to GitHub
echo ============================================
echo.

for /f "tokens=2 delims==" %%I in ('wmic os get localdatetime /value') do set datetime=%%I
set today=%datetime:~0,4%-%datetime:~4,2%-%datetime:~6,2%

echo   Date: %today%
echo   Step 1/2: Committing changes...
echo.

git add -A

git commit -m "%today% daily check-in" 2>nul
if %errorlevel% neq 0 (
    echo   [WARN] Nothing to commit. Did you save your changes?
    echo.
    pause
    exit /b 0
)

echo   Step 2/2: Pushing to GitHub...
git push

if %errorlevel% neq 0 (
    echo.
    echo   [ERROR] Push failed. Check your network.
    echo.
    pause
    exit /b 1
)

echo.
echo ============================================
echo   DONE! Go check your green dot:
echo   github.com/zyc-automation
echo ============================================
echo.
pause
