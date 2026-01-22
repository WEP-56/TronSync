# -*- mode: python ; coding: utf-8 -*-
import os
import sys

block_cipher = None

# PyWebView 相关的二进制文件和 DLL
pywebview_binaries = []
if sys.platform == 'win32':
    # 添加 PyWebView 需要的 DLL
    import webview
    webview_path = os.path.dirname(webview.__file__)
    
    # 查找 PyWebView 的 DLL 文件
    dll_files = [
        'Microsoft.Toolkit.Win32.WebView.dll',
        'Microsoft.Web.WebView2.Core.dll',
        'Microsoft.Web.WebView2.WinForms.dll',
        'Microsoft.Web.WebView2.Wpf.dll',
        'WebView2Loader.dll'
    ]
    
    for dll in dll_files:
        dll_path = os.path.join(webview_path, 'lib', dll)
        if os.path.exists(dll_path):
            pywebview_binaries.append((dll_path, '.'))

a = Analysis(
    ['run.py'],
    pathex=[],
    binaries=pywebview_binaries,  # 添加 PyWebView 的二进制文件
    datas=[
        ('frontend/dist', 'frontend/dist'),
        ('config.json', '.'),
    ],
    hiddenimports=[
        'flask',
        'flask_cors',
        'requests',
        'bs4',
        'webview',
        'webview.platforms.winforms',  # 添加 Windows 平台支持
        'webview.platforms.cef',       # 添加 CEF 支持
        'tkinter',
        'tkinter.filedialog',
        'PIL',
        'clr',                         # 添加 .NET 支持
        'System',
        'System.Windows.Forms',
        'System.Threading',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='TronSync',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # 不显示控制台窗口
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico' if os.path.exists('icon.ico') else None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='TronSync',
)
