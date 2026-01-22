@echo off
chcp 65001 >nul
title TronSync 运行时修复工具

:: 设置颜色（如果支持）
color 0A

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    TronSync 运行时修复工具                    ║
echo ╠══════════════════════════════════════════════════════════════╣
echo ║  如果 TronSync.exe 无法启动，此工具将自动安装所需的运行时库   ║
echo ║  这些是 Microsoft 官方组件，被数百万应用程序使用            ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo 💡 关于要安装的组件：
echo.
echo 📦 Visual C++ Redistributable
echo    ├─ Microsoft 官方运行时库
echo    ├─ 被以下知名软件使用：
echo    │  • Adobe Photoshop、Premiere Pro
echo    │  • Steam 游戏平台及大部分游戏
echo    │  • Microsoft Office、Visual Studio
echo    │  • 腾讯 QQ、微信、钉钉
echo    │  • 网易云音乐、爱奇艺、优酷
echo    └─ 安全性：Microsoft 数字签名，完全安全
echo.
echo 🌐 WebView2 Runtime  
echo    ├─ Microsoft Edge 浏览器内核
echo    ├─ 被以下知名软件使用：
echo    │  • Microsoft Teams、Outlook
echo    │  • WhatsApp Desktop、Spotify
echo    │  • 钉钉、企业微信
echo    │  • Visual Studio Code 部分功能
echo    │  • 大量现代桌面应用程序
echo    └─ 安全性：Windows 11 内置，Microsoft 官方组件
echo.
echo ✅ 这些组件安装后对系统有益无害，还能让其他软件运行更稳定
echo ⚡ 安装过程完全自动化，无需用户干预
echo.

:: 检查是否在正确的目录
if not exist "TronSync.exe" (
    echo ❌ 错误：未找到 TronSync.exe
    echo 请确保此脚本与 TronSync.exe 在同一目录下
    echo.
    pause
    exit /b 1
)

echo 🔍 正在检查运行环境...
echo.

:: 创建临时目录
set TEMP_DIR=%TEMP%\TronSync_Runtime_Fix
if not exist "%TEMP_DIR%" mkdir "%TEMP_DIR%"

:: 定义下载文件
set VC_REDIST_URL=https://aka.ms/vs/17/release/vc_redist.x64.exe
set WEBVIEW2_URL=https://go.microsoft.com/fwlink/p/?LinkId=2124703
set VC_REDIST_FILE=%TEMP_DIR%\vc_redist.x64.exe
set WEBVIEW2_FILE=%TEMP_DIR%\MicrosoftEdgeWebview2Setup.exe

echo 📥 正在下载运行时库...
echo.
echo 💡 下载说明：
echo    • 文件来源：Microsoft 官方服务器
echo    • 文件安全：具有 Microsoft 数字签名
echo    • 下载大小：约 15MB（两个文件总计）
echo    • 安装时间：通常 1-3 分钟
echo.

:: 下载 Visual C++ Redistributable
echo [1/2] 下载 Visual C++ Redistributable...
powershell -Command "& {try { Invoke-WebRequest -Uri '%VC_REDIST_URL%' -OutFile '%VC_REDIST_FILE%' -UseBasicParsing; Write-Host '✅ Visual C++ Redistributable 下载完成' } catch { Write-Host '❌ 下载失败，将打开浏览器手动下载'; Start-Process '%VC_REDIST_URL%' }}"

:: 下载 WebView2 Runtime
echo [2/2] 下载 WebView2 Runtime...
powershell -Command "& {try { Invoke-WebRequest -Uri '%WEBVIEW2_URL%' -OutFile '%WEBVIEW2_FILE%' -UseBasicParsing; Write-Host '✅ WebView2 Runtime 下载完成' } catch { Write-Host '❌ 下载失败，将打开浏览器手动下载'; Start-Process '%WEBVIEW2_URL%' }}"

echo.
echo 🔧 正在安装运行时库...
echo.
echo 💡 安装说明：
echo    • 这些是系统级组件，需要管理员权限
echo    • 如果弹出 UAC 提示，请点击"是"
echo    • 安装过程由 Microsoft 安装程序处理，完全安全
echo    • 安装后将提升整个系统的软件兼容性
echo.

:: 安装 Visual C++ Redistributable
if exist "%VC_REDIST_FILE%" (
    echo [1/2] 安装 Visual C++ Redistributable...
    echo 💡 正在安装 Microsoft Visual C++ 运行时库
    echo    这是 Adobe、Steam、Office 等软件的必需组件
    echo    请在弹出的安装程序中点击"安装"或"修复"
    "%VC_REDIST_FILE%" /quiet /norestart
    if errorlevel 1 (
        echo ⚠️ 静默安装失败，启动交互式安装...
        echo 💡 请在安装程序中点击"我同意"和"安装"
        "%VC_REDIST_FILE%"
        echo 请完成安装后按任意键继续...
        pause >nul
    ) else (
        echo ✅ Visual C++ Redistributable 安装完成
        echo 💡 您的系统现在可以运行更多现代应用程序了
    )
) else (
    echo ❌ Visual C++ Redistributable 下载失败
    echo 💡 这是 Microsoft 官方组件，请放心手动下载安装
    echo 下载地址: %VC_REDIST_URL%
    echo 按任意键继续...
    pause >nul
)

echo.

:: 安装 WebView2 Runtime
if exist "%WEBVIEW2_FILE%" (
    echo [2/2] 安装 WebView2 Runtime...
    echo 💡 正在安装 Microsoft Edge WebView2 运行时
    echo    这是 Teams、WhatsApp、钉钉等软件的必需组件
    echo    Windows 11 系统已内置，此安装确保兼容性
    "%WEBVIEW2_FILE%" /silent /install
    if errorlevel 1 (
        echo ⚠️ 静默安装失败，启动交互式安装...
        echo 💡 请在安装程序中点击"安装"
        "%WEBVIEW2_FILE%"
        echo 请完成安装后按任意键继续...
        pause >nul
    ) else (
        echo ✅ WebView2 Runtime 安装完成
        echo 💡 您的系统现在支持最新的 Web 技术应用了
    )
) else (
    echo ❌ WebView2 Runtime 下载失败
    echo 💡 这是 Microsoft Edge 浏览器内核，完全安全
    echo 下载地址: %WEBVIEW2_URL%
    echo 按任意键继续...
    pause >nul
)

echo.
echo 🧹 清理临时文件...
if exist "%TEMP_DIR%" rmdir /s /q "%TEMP_DIR%" 2>nul

echo.
echo ✅ 运行时库安装完成！
echo.
echo 🎉 恭喜！您的系统现在已具备：
echo    ✅ Visual C++ Redistributable - 支持现代 C++ 应用
echo    ✅ WebView2 Runtime - 支持现代 Web 应用
echo    ✅ 更好的软件兼容性和稳定性
echo.
echo 💡 这些组件的其他好处：
echo    • 让 Adobe 软件运行更稳定
echo    • 提升游戏兼容性（Steam 平台游戏）
echo    • 支持更多办公软件（Office、Teams 等）
echo    • 提升整体系统现代化程度
echo.
echo 🚀 正在启动 TronSync...
echo.

:: 启动 TronSync
start "" "TronSync.exe"

:: 等待一下看是否成功启动
timeout /t 3 >nul

:: 检查进程是否在运行
tasklist /FI "IMAGENAME eq TronSync.exe" 2>nul | find /I "TronSync.exe" >nul
if errorlevel 1 (
    echo.
    echo ⚠️ TronSync 可能未成功启动
    echo.
    echo 💡 如果仍有问题，请尝试：
    echo 1. 重启电脑后再次运行 TronSync.exe
    echo 2. 以管理员身份运行 TronSync.exe
    echo 3. 检查杀毒软件是否拦截了程序
    echo 4. 确保 Windows 系统已更新到最新版本
    echo.
    echo 按任意键退出...
    pause >nul
) else (
    echo ✅ TronSync 启动成功！
    echo.
    echo 💡 提示：如果以后遇到同样问题，可以再次运行此脚本
    echo.
    timeout /t 5
)

exit