@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
cd /d "%~dp0"

:: =============================================
::   newday.bat — 一键创建今天的学习笔记模板
::   用法：每天双击一次，自动生成 matlab + ros2 笔记
:: =============================================

:: 中文 Windows 上 %date% 格式: 2026/08/12 周三
set year=%date:~0,4%
set month=%date:~5,2%
set day=%date:~8,2%
set weekday=%date:~12%

set today=%year%-%month%-%day%
set month_dir=%year%-%month%

echo.
echo   ╔══════════════════════════════════╗
echo   ║     New Day · %today%  %weekday%      ║
echo   ╚══════════════════════════════════╝
echo.

:: ---------- MATLAB 笔记 ----------
set matlab_md=matlab\%month_dir%\%day%.md

if not exist "matlab\%month_dir%" mkdir "matlab\%month_dir%"

if exist "%matlab_md%" (
    for %%A in ("%matlab_md%") do set fsize=%%~zA
    if !fsize! GTR 200 (
        echo   [SKIP] matlab/%month_dir%/%day%.md 已有内容，跳过
    ) else (
        echo   [OK]   matlab/%month_dir%/%day%.md 模板已生成
        call :write_matlab_template
    )
) else (
    echo   [OK]   matlab/%month_dir%/%day%.md 模板已生成
    call :write_matlab_template
)

:: ---------- ROS2 笔记 ----------
set ros2_md=ros2\%month_dir%\%day%.md

if not exist "ros2\%month_dir%" mkdir "ros2\%month_dir%"

if exist "%ros2_md%" (
    for %%A in ("%ros2_md%") do set fsize=%%~zA
    if !fsize! GTR 200 (
        echo   [SKIP] ros2/%month_dir%/%day%.md 已有内容，跳过
    ) else (
        echo   [OK]   ros2/%month_dir%/%day%.md 模板已生成
        call :write_ros2_template
    )
) else (
    echo   [OK]   ros2/%month_dir%/%day%.md 模板已生成
    call :write_ros2_template
)

:: ---------- Python 笔记 ----------
set python_md=python\%month_dir%\%day%.md

if not exist "python\%month_dir%" mkdir "python\%month_dir%"

if exist "%python_md%" (
    for %%A in ("%python_md%") do set fsize=%%~zA
    if !fsize! GTR 200 (
        echo   [SKIP] python/%month_dir%/%day%.md 已有内容，跳过
    ) else (
        echo   [OK]   python/%month_dir%/%day%.md 模板已生成
        call :write_python_template
    )
) else (
    echo   [OK]   python/%month_dir%/%day%.md 模板已生成
    call :write_python_template
)

:: ---------- C 语言笔记 ----------
set c_md=c\%month_dir%\%day%.md

if not exist "c\%month_dir%" mkdir "c\%month_dir%"

if exist "%c_md%" (
    for %%A in ("%c_md%") do set fsize=%%~zA
    if !fsize! GTR 200 (
        echo   [SKIP] c/%month_dir%/%day%.md 已有内容，跳过
    ) else (
        echo   [OK]   c/%month_dir%/%day%.md 模板已生成
        call :write_c_template
    )
) else (
    echo   [OK]   c/%month_dir%/%day%.md 模板已生成
    call :write_c_template
)

echo.
echo   一切就绪，开始今天的学习吧！
echo.

:: 打开 daily-code 文件夹
start "" "%~dp0"

pause
exit /b 0

:: ============ 模板函数 ============

:write_matlab_template
(
echo # %today% · %weekday%
echo.
echo ## 今天做了什么
echo.
echo - 
echo.
echo ## 踩坑 / 收获
echo.
echo - 
echo.
echo ## 明天计划
echo.
echo - 
echo.
echo ## 代码文件
echo.
echo - `control-sim/`
) > "%matlab_md%"
goto :eof

:write_ros2_template
(
echo # %today% · %weekday%
echo.
echo ## 今天做了什么
echo.
echo - 
echo.
echo ## 踩坑 / 收获
echo.
echo - 
echo.
echo ## 明天计划
echo.
echo - 
) > "%ros2_md%"
goto :eof

:write_python_template
(
echo # %today% · %weekday%
echo.
echo ## 今天做了什么
echo.
echo - 
echo.
echo ## 踩坑 / 收获
echo.
echo - 
echo.
echo ## 明天计划
echo.
echo - 
) > "%python_md%"
goto :eof

:write_c_template
(
echo # %today% · %weekday%
echo.
echo ## 今天做了什么
echo.
echo - 
echo.
echo ## 踩坑 / 收获
echo.
echo - 
echo.
echo ## 明天计划
echo.
echo - 
) > "%c_md%"
goto :eof
