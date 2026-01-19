# TronSync 打包完整指南

## 📋 目录

- [环境要求](#环境要求)
- [快速打包](#快速打包)
- [打包配置说明](#打包配置说明)
- [打包后的目录结构](#打包后的目录结构)
- [分发说明](#分发说明)
- [常见问题](#常见问题)
- [优化建议](#优化建议)
- [测试清单](#测试清单)
- [版本发布流程](#版本发布流程)

---

## 环境要求

- Python 3.8+
- Node.js 16+
- 已安装所有依赖（requirements.txt）

## 快速打包

### 方法一：使用打包脚本（推荐）⭐

**一键打包：**

```bash
# 直接双击运行
build.bat
```

脚本会自动完成以下步骤：
1. ✅ 检查并安装 PyInstaller
2. ✅ 构建前端（npm run build）
3. ✅ 使用 PyInstaller 打包
4. ✅ 清理临时文件

打包完成后，可执行文件位于：`dist/TronSync/TronSync.exe`

### 方法二：手动打包

```bash
# 1. 安装 PyInstaller
pip install pyinstaller

# 2. 构建前端
cd frontend
npm run build
cd ..

# 3. 打包
pyinstaller build.spec --clean

# 4. 查看结果
# 可执行文件位于 dist/TronSync/TronSync.exe
```

---

## 打包配置说明

### build.spec 配置详解

```python
# 数据文件配置
datas=[
    ('frontend/dist', 'frontend/dist'),  # 前端构建产物
    ('config.json', '.'),                # 配置文件模板
]

# 隐式导入的模块（防止打包遗漏）
hiddenimports=[
    'flask',           # Web 框架
    'flask_cors',      # 跨域支持
    'requests',        # HTTP 请求
    'bs4',            # HTML 解析
    'webview',        # 桌面窗口
    'tkinter',        # 文件对话框
    'PIL',            # 图像处理
]

# GUI 应用配置
console=False  # 不显示控制台窗口
```

### 自定义图标

如果要添加自定义图标：

1. 准备一个 `.ico` 文件（推荐 256x256）
2. 命名为 `icon.ico` 并放在项目根目录
3. 重新运行 `build.bat`

---

## 打包后的目录结构

```
dist/
└── TronSync/
    ├── TronSync.exe          # 主程序（双击运行）
    ├── frontend/
    │   └── dist/             # 前端静态文件
    ├── config.json           # 配置文件
    ├── _internal/            # Python 运行时和依赖
    └── [其他依赖文件]
```

---

## 分发说明

### 创建发布包

**步骤：**

1. **压缩文件夹**
   ```bash
   # 使用 7-Zip 或 WinRAR 压缩
   # 将 dist/TronSync 文件夹压缩为 TronSync-v1.0.0.zip
   ```

2. **测试压缩包**
   - 解压到新位置
   - 运行 TronSync.exe 确保正常工作

3. **准备发布说明**
   - 复制 `RELEASE_README.md` 的内容
   - 添加更新日志

### 上传到 GitHub

1. 在 GitHub 仓库创建新的 Release
2. 标签版本：`vX.X.X`
3. 发布标题：`TronSync vX.X.X`
4. 上传 `TronSync-v1.0.0.zip`
5. 添加发布说明（使用 RELEASE_README.md 的内容）

### 完整版分发

将整个 `dist/TronSync` 文件夹打包成 zip，用户解压后直接运行 `TronSync.exe`

**优点：**
- 启动速度快
- 文件结构清晰
- 易于调试

### 单文件打包（可选）

如果需要单文件版本，修改 `build.spec`：

```python
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,      # 添加这行
    a.zipfiles,      # 添加这行
    a.datas,         # 添加这行
    [],
    name='TronSync',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    icon='icon.ico' if os.path.exists('icon.ico') else None,
)

# 删除 COLLECT 部分
```

**注意：** 单文件版本启动较慢，因为需要解压临时文件。

---

## 常见问题

### 1. PyInstaller 未安装

**解决：**
```bash
pip install pyinstaller
```

### 2. 前端构建失败

**解决：**
```bash
cd frontend
npm install
npm run build
cd ..
```

### 3. 打包后运行报错 "Failed to execute script"

**原因：** 缺少依赖或路径问题

**解决：**
- 检查 `hiddenimports` 是否包含所有依赖
- 临时使用 `console=True` 查看详细错误信息
- 在 `build.spec` 中添加缺失的模块

### 4. 前端页面无法加载

**原因：** 静态文件路径问题

**解决：**
- 确保 `frontend/dist` 已正确构建
- 检查 `build.spec` 中的 `datas` 配置
- 验证 `app.py` 中的静态文件路径

### 5. 打包文件过大

**原因：** 包含了不必要的依赖

**解决：**
- 使用虚拟环境，只安装必要的包
- 在 `build.spec` 中添加 `excludes` 排除不需要的模块
- 参考下面的"优化建议"

### 6. 杀毒软件误报

**原因：** PyInstaller 打包的程序可能被误报

**解决：**
- 添加到杀毒软件白名单
- 使用代码签名证书（需要购买）
- 向杀毒软件厂商报告误报

### 7. 文件夹选择对话框不显示

**原因：** tkinter 未正确打包

**解决：**
- 确保 `hiddenimports` 包含 `tkinter`
- 检查 Python 安装是否包含 tkinter

---

## 优化建议

### 减小文件大小

**1. 使用 UPX 压缩**（已启用）
```python
upx=True
```

**2. 排除不需要的模块**
```python
excludes=[
    'matplotlib',  # 如果不需要绘图
    'numpy',       # 如果不需要数值计算
    'pandas',      # 如果不需要数据分析
    'PIL',         # 如果不需要图像处理
]
```

**3. 使用虚拟环境**
```bash
# 创建干净的虚拟环境
python -m venv venv_build
venv_build\Scripts\activate

# 只安装必要的依赖
pip install -r requirements.txt

# 在虚拟环境中打包
pyinstaller build.spec --clean
```

**4. 清理 Python 缓存**
```bash
# 删除 __pycache__ 文件夹
del /s /q __pycache__
```

### 提升启动速度

1. **使用文件夹模式**（而非单文件）✅ 已采用
2. **减少隐式导入** - 只导入必要的模块
3. **延迟加载大型模块** - 在需要时才导入
4. **优化前端资源** - 压缩 JS/CSS 文件

### 提升用户体验

1. **添加启动画面** - 显示加载进度
2. **添加错误日志** - 方便问题排查
3. **添加自动更新** - 检查新版本
4. **优化图标** - 使用高质量图标

---

## 测试清单

打包完成后，请测试以下功能：

### 基础功能
- [ ] 应用能正常启动
- [ ] 窗口大小和位置正确
- [ ] 界面显示正常

### 登录功能
- [ ] 登录功能正常
- [ ] 记住密码功能正常
- [ ] 自动登录功能正常

### 数据加载
- [ ] 个人信息显示正常
- [ ] 课程列表加载正常
- [ ] 课程表显示正常
- [ ] 公告加载正常
- [ ] 文件列表加载正常

### 交互功能
- [ ] 课程表周数切换正常
- [ ] 学年学期切换正常
- [ ] 公告展开/折叠正常
- [ ] 文件夹浏览正常
- [ ] 面包屑导航正常

### 下载功能
- [ ] 文件下载功能正常
- [ ] 下载路径设置正常
- [ ] 文件夹选择对话框正常

### 设置功能
- [ ] 设置保存和加载正常
- [ ] 主题切换正常（浅色/深色）
- [ ] 紧凑模式正常
- [ ] 缓存清除正常

### 性能测试
- [ ] 启动速度可接受（< 5秒）
- [ ] 内存占用合理（< 200MB）
- [ ] 响应速度流畅

### 异常处理
- [ ] 网络断开时提示正确
- [ ] 登录失败时提示正确
- [ ] 数据加载失败时提示正确

---

## 版本发布流程

### 1. 准备发布

```bash
# 更新代码
git pull

# 检查是否有未提交的更改
git status
```

### 2. 更新版本号

编辑 `frontend/src/views/Home.vue`：
```vue
<p class="app-version">版本 1.1.0</p>  <!-- 更新这里 -->
```

### 3. 构建前端

```bash
cd frontend
npm run build
cd ..
```

### 4. 打包应用

```bash
build.bat
```

### 5. 测试

```bash
cd dist\TronSync
TronSync.exe
# 完整测试所有功能
cd ..\..
```

### 6. 创建发布包

```bash
# 压缩 dist/TronSync 为 TronSync-v1.0.1.zip
# 使用 7-Zip 或 WinRAR
```

### 7. 准备发布说明

创建 `CHANGELOG.md`：
```markdown
## v1.0.1 (2025-01-17)

### 新增
- 添加了 XXX 功能

### 修复
- 修复了 XXX 问题

### 优化
- 优化了 XXX 性能
```

### 8. 上传到 GitHub Release

1. 访问 GitHub 仓库
2. 点击 "Releases" → "Create a new release"
3. 填写信息：
   - Tag: `v1.0.1`
   - Title: `TronSync v1.0.1`
   - Description: 复制 CHANGELOG 和 RELEASE_README 内容
4. 上传 `TronSync-v1.0.1.zip`
5. 点击 "Publish release"

### 9. 通知用户

- 在相关群组/论坛发布更新通知
- 提供下载链接和更新说明

---

## 完整工作流示例

```bash
# ========================================
# TronSync 发布完整流程
# ========================================

# 1. 更新代码
git pull
git status

# 2. 更新版本号
# 手动编辑 frontend/src/views/Home.vue

# 3. 提交更改
git add .
git commit -m "Release v1.0.1"
git push

# 4. 构建和打包
build.bat

# 5. 测试
cd dist\TronSync
TronSync.exe
# 完整测试...
cd ..\..

# 6. 创建发布包
# 压缩 dist/TronSync 为 zip

# 7. 创建 GitHub Release
# 在 GitHub 网页操作

# 8. 完成！
```

---

## 高级配置

### 添加版本信息

创建 `version_info.txt`：
```python
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1, 0, 0, 0),
    prodvers=(1, 0, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo([
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'TronSync'),
        StringStruct(u'FileDescription', u'澳门城市大学校园助手'),
        StringStruct(u'FileVersion', u'1.0.0.0'),
        StringStruct(u'InternalName', u'TronSync'),
        StringStruct(u'LegalCopyright', u'Copyright (c) 2025'),
        StringStruct(u'OriginalFilename', u'TronSync.exe'),
        StringStruct(u'ProductName', u'TronSync'),
        StringStruct(u'ProductVersion', u'1.0.0.0')])
    ]),
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
```

在 `build.spec` 中引用：
```python
exe = EXE(
    ...
    version='version_info.txt',
    ...
)
```

### 添加启动画面

1. 准备启动画面图片 `splash.png`
2. 修改 `build.spec`：
```python
splash = Splash(
    'splash.png',
    binaries=a.binaries,
    datas=a.datas,
    text_pos=(10, 50),
    text_size=12,
    text_color='black'
)
```

---

## 技术支持

### 获取帮助

- **GitHub Issues**: 提交问题和建议
- **文档**: 查看项目文档
- **社区**: 加入讨论群组

### 贡献代码

欢迎提交 Pull Request！

1. Fork 项目
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

---

## 附录

### 相关文件

- `build.spec` - PyInstaller 配置
- `build.bat` - 打包脚本
- `requirements.txt` - Python 依赖
- `RELEASE_README.md` - 用户说明

### 有用的命令

```bash
# 查看打包日志
pyinstaller build.spec --clean --log-level DEBUG

# 分析依赖
pyi-archive_viewer dist/TronSync/TronSync.exe

# 测试单个模块
python -c "import flask; print(flask.__version__)"
```

### 参考资源

- [PyInstaller 官方文档](https://pyinstaller.org/)
- [PyWebView 文档](https://pywebview.flowrl.com/)
- [Flask 文档](https://flask.palletsprojects.com/)

---

**祝打包顺利！** 🎉

如有问题，请查看常见问题部分或提交 Issue。

