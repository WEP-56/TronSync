# GitHub 上传指南

## 首次上传到 GitHub

### 1. 在 GitHub 上创建仓库

1. 访问 [GitHub](https://github.com)
2. 点击右上角的 "+" → "New repository"
3. 填写信息：
   - Repository name: `TronSync`
   - Description: `澳门城市大学校园助手 - 桌面客户端`
   - 选择 Public 或 Private
   - **不要**勾选 "Initialize this repository with a README"
4. 点击 "Create repository"

### 2. 初始化本地仓库

在项目根目录打开终端：

```bash
# 初始化 Git 仓库
git init

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit: TronSync v1.0.0"

# 添加远程仓库（替换为你的 GitHub 用户名）
git remote add origin https://github.com/你的用户名/TronSync.git

# 推送到 GitHub
git branch -M main
git push -u origin main
```

### 3. 验证上传

访问你的 GitHub 仓库页面，应该能看到所有文件。

## 后续更新

### 提交更改

```bash
# 查看修改的文件
git status

# 添加修改的文件
git add .

# 提交修改
git commit -m "描述你的修改"

# 推送到 GitHub
git push
```

### 创建版本标签

```bash
# 创建标签
git tag -a v1.0.1 -m "版本 1.0.1"

# 推送标签
git push origin v1.0.1
```

## 发布 Release

### 方法一：通过 GitHub 网页

1. 访问你的仓库
2. 点击 "Releases" → "Create a new release"
3. 填写信息：
   - Tag: `v1.0.0`
   - Release title: `TronSync v1.0.0`
   - Description: 复制 CHANGELOG 内容
4. 上传打包好的 `TronSync-v1.0.0.zip`
5. 点击 "Publish release"

### 方法二：使用 GitHub CLI

```bash
# 安装 GitHub CLI
# https://cli.github.com/

# 登录
gh auth login

# 创建 release
gh release create v1.0.0 TronSync-v1.0.0.zip --title "TronSync v1.0.0" --notes "首次发布"
```

## 常用 Git 命令

### 查看状态
```bash
git status
```

### 查看提交历史
```bash
git log --oneline
```

### 撤销修改
```bash
# 撤销工作区的修改
git checkout -- 文件名

# 撤销暂存区的修改
git reset HEAD 文件名
```

### 分支管理
```bash
# 创建分支
git checkout -b feature/new-feature

# 切换分支
git checkout main

# 合并分支
git merge feature/new-feature

# 删除分支
git branch -d feature/new-feature
```

### 拉取更新
```bash
# 拉取远程更新
git pull

# 拉取并变基
git pull --rebase
```

## 忽略文件

`.gitignore` 已经配置好，会自动忽略：

- `__pycache__/` - Python 缓存
- `node_modules/` - Node.js 依赖
- `dist/` - 打包输出
- `config.json` - 用户配置（包含密码）
- `.venv/` - 虚拟环境
- `.idea/` - IDE 配置

## 协作开发

### Fork 工作流

1. **Fork 项目**：在 GitHub 上点击 Fork
2. **克隆 Fork**：`git clone https://github.com/你的用户名/TronSync.git`
3. **添加上游**：`git remote add upstream https://github.com/原作者/TronSync.git`
4. **同步上游**：
   ```bash
   git fetch upstream
   git merge upstream/main
   ```
5. **创建分支**：`git checkout -b feature/your-feature`
6. **提交修改**：`git commit -m "描述"`
7. **推送分支**：`git push origin feature/your-feature`
8. **创建 PR**：在 GitHub 上创建 Pull Request

## 自动化构建

项目已配置 GitHub Actions（`.github/workflows/build.yml`）：

- 当推送标签时自动构建
- 自动创建 Release
- 自动上传打包文件

使用方法：
```bash
# 创建并推送标签
git tag -a v1.0.1 -m "版本 1.0.1"
git push origin v1.0.1

# GitHub Actions 会自动构建并发布
```

## 注意事项

### 敏感信息

- ✅ **已忽略** `config.json`（包含用户密码）
- ✅ **已提供** `config.json.example` 作为模板
- ⚠️ **不要提交**任何包含真实账号密码的文件

### 大文件

- Git 不适合存储大文件（>100MB）
- 如果需要存储大文件，使用 [Git LFS](https://git-lfs.github.com/)

### 提交信息规范

使用清晰的提交信息：

```bash
# 好的例子
git commit -m "feat: 添加课程表周数切换功能"
git commit -m "fix: 修复公告未读计数错误"
git commit -m "docs: 更新 README 安装说明"

# 避免
git commit -m "update"
git commit -m "修改"
```

提交类型：
- `feat`: 新功能
- `fix`: 修复 bug
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 重构
- `test`: 测试相关
- `chore`: 构建/工具相关

## 获取帮助

- [Git 官方文档](https://git-scm.com/doc)
- [GitHub 文档](https://docs.github.com/)
- [Git 教程](https://www.liaoxuefeng.com/wiki/896043488029600)

## 问题排查

### 推送失败

```bash
# 如果推送失败，先拉取
git pull --rebase
git push
```

### 合并冲突

```bash
# 查看冲突文件
git status

# 手动解决冲突后
git add .
git commit -m "解决合并冲突"
```

### 撤销提交

```bash
# 撤销最后一次提交（保留修改）
git reset --soft HEAD~1

# 撤销最后一次提交（丢弃修改）
git reset --hard HEAD~1
```

---

祝你上传顺利！如有问题，欢迎提 Issue。
