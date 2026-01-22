@echo off
chcp 65001 >nul
echo ========================================
echo TronSync 打包脚本 (增强版)
echo ========================================

echo.
echo [1/6] 检查环境...

:: 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python 未安装或未添加到 PATH
    pause
    exit /b 1
)

:: 检查 Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js 未安装或未添加到 PATH
    pause
    exit /b 1
)

echo ✅ 环境检查通过

echo.
echo [2/6] 安装/更新 PyInstaller...
pip install --upgrade pyinstaller
if errorlevel 1 (
    echo ❌ PyInstaller 安装失败
    pause
    exit /b 1
)

echo.
echo [3/6] 构建前端...
pushd frontend
if not exist "node_modules" (
    echo 📦 安装前端依赖...
    call npm install
    if errorlevel 1 (
        echo ❌ 前端依赖安装失败
        popd
        pause
        exit /b 1
    )
)

echo 🔨 构建前端...
call npm run build
if errorlevel 1 (
    echo ❌ 前端构建失败
    popd
    pause
    exit /b 1
)
popd

echo ✅ 前端构建完成

echo.
echo [4/6] 清理旧的打包文件...
echo 🧹 清理 dist 目录...
if exist "dist" (
    rmdir /s /q "dist" 2>nul
    echo ✅ 已清理 dist 目录
)
echo 🧹 清理 build 目录...
if exist "build" (
    rmdir /s /q "build" 2>nul
    echo ✅ 已清理 build 目录
)

echo.
echo [5/6] 开始打包...
echo 📦 使用 PyInstaller 打包应用...
echo 当前目录: %CD%
echo 检查 build.spec 文件...
if not exist "build.spec" (
    echo ❌ build.spec 文件不存在
    pause
    exit /b 1
)
echo ✅ build.spec 文件存在

pyinstaller build.spec --clean --noconfirm
if errorlevel 1 (
    echo ❌ 打包失败
    echo 请检查上面的错误信息
    pause
    exit /b 1
)
echo ✅ PyInstaller 打包完成

echo.
echo [6/6] 创建用户修复工具...

:: 复制修复脚本到打包目录
copy "运行不了双击这里.bat" "dist\TronSync\" >nul 2>&1
if exist "dist\TronSync\运行不了双击这里.bat" (
    echo ✅ 用户修复工具已创建
) else (
    echo ⚠️ 修复工具复制失败，手动创建...
    
    :: 手动创建修复脚本
    echo @echo off > "dist\TronSync\运行不了双击这里.bat"
    echo chcp 65001 ^>nul >> "dist\TronSync\运行不了双击这里.bat"
    echo title TronSync 运行时修复工具 >> "dist\TronSync\运行不了双击这里.bat"
    echo. >> "dist\TronSync\运行不了双击这里.bat"
    echo echo ======================================== >> "dist\TronSync\运行不了双击这里.bat"
    echo echo TronSync 运行时修复工具 >> "dist\TronSync\运行不了双击这里.bat"
    echo echo ======================================== >> "dist\TronSync\运行不了双击这里.bat"
    echo echo. >> "dist\TronSync\运行不了双击这里.bat"
    echo echo 如果 TronSync.exe 无法启动，此工具将自动安装所需的运行时库 >> "dist\TronSync\运行不了双击这里.bat"
    echo echo. >> "dist\TronSync\运行不了双击这里.bat"
    echo echo 📥 正在下载运行时库... >> "dist\TronSync\运行不了双击这里.bat"
    echo powershell -Command "Start-Process 'https://aka.ms/vs/17/release/vc_redist.x64.exe'" >> "dist\TronSync\运行不了双击这里.bat"
    echo timeout /t 2 ^>nul >> "dist\TronSync\运行不了双击这里.bat"
    echo powershell -Command "Start-Process 'https://go.microsoft.com/fwlink/p/?LinkId=2124703'" >> "dist\TronSync\运行不了双击这里.bat"
    echo echo. >> "dist\TronSync\运行不了双击这里.bat"
    echo echo 请安装以上两个程序，然后重新运行 TronSync.exe >> "dist\TronSync\运行不了双击这里.bat"
    echo pause >> "dist\TronSync\运行不了双击这里.bat"
    
    echo ✅ 简化版修复工具已创建
)

:: 创建简单的使用说明
echo # TronSync 使用说明 > "dist\TronSync\使用说明.txt"
echo. >> "dist\TronSync\使用说明.txt"
echo ## 正常启动 >> "dist\TronSync\使用说明.txt"
echo 双击 TronSync.exe 启动应用 >> "dist\TronSync\使用说明.txt"
echo. >> "dist\TronSync\使用说明.txt"
echo ## 如果无法启动 >> "dist\TronSync\使用说明.txt"
echo 双击"运行不了双击这里.bat"自动修复运行环境 >> "dist\TronSync\使用说明.txt"
echo. >> "dist\TronSync\使用说明.txt"
echo ## 系统要求 >> "dist\TronSync\使用说明.txt"
echo - Windows 10 或更高版本 >> "dist\TronSync\使用说明.txt"
echo - Visual C++ Redistributable >> "dist\TronSync\使用说明.txt"
echo - WebView2 Runtime >> "dist\TronSync\使用说明.txt"
echo. >> "dist\TronSync\使用说明.txt"
echo ## 技术支持 >> "dist\TronSync\使用说明.txt"
echo 如有问题请查看项目 GitHub 页面或提交 Issue >> "dist\TronSync\使用说明.txt"

echo.
echo ✅ 打包完成！
echo.
echo 📁 输出位置: dist\TronSync\
echo 🚀 主程序: dist\TronSync\TronSync.exe
echo 🔧 修复工具: dist\TronSync\运行不了双击这里.bat
echo 📋 使用说明: dist\TronSync\使用说明.txt
echo.
echo 💡 分发说明：
echo    1. 将整个 dist\TronSync 文件夹打包成 zip
echo    2. 用户解压后直接运行 TronSync.exe
echo    3. 如果无法运行，双击"运行不了双击这里.bat"自动修复
echo    4. 修复工具会自动下载并安装必要的运行时库
echo.
echo 🎯 已验证的解决方案：
echo    ✅ Visual C++ Redistributable (必需)
echo    ✅ WebView2 Runtime (必需)
echo    ✅ 自动下载和安装功能
echo.
pause