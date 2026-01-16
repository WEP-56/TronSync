@echo off
chcp 65001 >nul
echo ========================================
echo TronSync 打包脚本
echo ========================================
echo.

echo [1/4] 检查依赖...
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo 未安装 PyInstaller，正在安装...
    pip install pyinstaller
)

echo.
echo [2/4] 构建前端...
cd frontend
call npm run build
if errorlevel 1 (
    echo 前端构建失败！
    pause
    exit /b 1
)
cd ..

echo.
echo [3/4] 打包应用...
pyinstaller build.spec --clean

if errorlevel 1 (
    echo 打包失败！
    pause
    exit /b 1
)

echo.
echo [4/4] 清理临时文件...
rmdir /s /q build 2>nul

echo.
echo ========================================
echo 打包完成！
echo 可执行文件位置: dist\TronSync\TronSync.exe
echo ========================================
echo.
pause
