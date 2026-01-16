# 贡献指南

感谢你对 TronSync 项目的关注！

## 如何贡献

### 报告问题

如果你发现了 bug 或有功能建议：

1. 在 [Issues](https://github.com/你的用户名/TronSync/issues) 中搜索是否已有相关问题
2. 如果没有，创建新的 Issue，详细描述：
   - 问题的具体表现
   - 复现步骤
   - 预期行为
   - 实际行为
   - 系统环境（Windows 版本、Python 版本等）

### 提交代码

1. **Fork 项目**
   ```bash
   # 在 GitHub 上点击 Fork 按钮
   ```

2. **克隆你的 Fork**
   ```bash
   git clone https://github.com/你的用户名/TronSync.git
   cd TronSync
   ```

3. **创建分支**
   ```bash
   git checkout -b feature/your-feature-name
   # 或
   git checkout -b fix/your-bug-fix
   ```

4. **进行修改**
   - 遵循现有的代码风格
   - 添加必要的注释
   - 确保代码可以正常运行

5. **测试你的修改**
   ```bash
   # 运行应用测试
   python run.py
   
   # 测试打包
   build.bat
   ```

6. **提交修改**
   ```bash
   git add .
   git commit -m "描述你的修改"
   ```

7. **推送到你的 Fork**
   ```bash
   git push origin feature/your-feature-name
   ```

8. **创建 Pull Request**
   - 在 GitHub 上打开你的 Fork
   - 点击 "New Pull Request"
   - 详细描述你的修改

## 代码规范

### Python 代码

- 遵循 PEP 8 规范
- 使用有意义的变量名
- 添加必要的文档字符串

```python
def example_function(param1, param2):
    """
    函数的简短描述
    
    Args:
        param1: 参数1的描述
        param2: 参数2的描述
    
    Returns:
        返回值的描述
    """
    pass
```

### JavaScript/Vue 代码

- 使用 2 空格缩进
- 使用 const/let，避免使用 var
- 组件名使用 PascalCase
- 方法名使用 camelCase

```javascript
// 好的例子
const userName = 'example'
const getUserInfo = () => {
  // ...
}

// 避免
var user_name = 'example'
```

## 开发环境设置

### 前端开发

```bash
cd frontend
npm run dev
```

前端会在 `http://localhost:5173` 运行

### 后端开发

```bash
python app.py
```

后端会在 `http://127.0.0.1:5000` 运行

### 桌面应用开发

```bash
python run.py
```

## 项目结构

```
TronSync/
├── api/              # 后端 API（爬虫逻辑）
├── core/             # 核心功能（配置、会话管理）
├── models/           # 数据模型
├── frontend/         # Vue 3 前端
│   ├── src/
│   │   ├── api/      # 前端 API 调用
│   │   ├── utils/    # 工具函数
│   │   └── views/    # 页面组件
│   └── dist/         # 构建输出
├── app.py            # Flask 应用
├── run.py            # PyWebView 启动器
├── build.spec        # PyInstaller 配置
└── build.bat         # 打包脚本
```

## 注意事项

### 敏感信息

- **不要提交** `config.json` 文件（包含用户凭证）
- **不要提交** 任何包含真实账号密码的文件
- 使用 `config.json.example` 作为配置模板

### 爬虫规范

- 添加合理的请求延迟
- 使用浏览器 User-Agent
- 尊重网站的 robots.txt
- 不要进行高频请求

### 测试

在提交 PR 前，请确保：

- [ ] 应用可以正常启动
- [ ] 登录功能正常
- [ ] 主要功能（课程表、公告、文件）正常
- [ ] 没有控制台错误
- [ ] 打包后的应用可以运行

## 版本发布

版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)：

- **主版本号**：不兼容的 API 修改
- **次版本号**：向下兼容的功能性新增
- **修订号**：向下兼容的问题修正

例如：`v1.2.3`

## 获取帮助

如果你在贡献过程中遇到问题：

- 查看 [QUICKSTART.md](QUICKSTART.md) 了解构建流程
- 在 Issues 中提问
- 查看已有的 Pull Requests

## 行为准则

- 尊重他人
- 保持友善和专业
- 接受建设性的批评
- 关注对社区最有利的事情

感谢你的贡献！🎉
