"""
TronSync启动器
使用PyWebView创建桌面应用窗口，Flask作为后端服务
"""
import webview
import threading
import time
import sys
import logging
from tkinter import filedialog
import tkinter as tk

from app import app

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class API:
    """PyWebView API 类，用于前端调用桌面功能"""
    
    def select_folder(self):
        """选择文件夹"""
        try:
            # 创建隐藏的 Tk 窗口
            root = tk.Tk()
            root.withdraw()
            root.attributes('-topmost', True)
            
            # 打开文件夹选择对话框
            folder_path = filedialog.askdirectory(
                title='选择下载文件夹',
                parent=root
            )
            
            root.destroy()
            
            if folder_path:
                logger.info(f"✅ 选择的文件夹: {folder_path}")
                return {'success': True, 'path': folder_path}
            else:
                return {'success': False, 'message': '未选择文件夹'}
                
        except Exception as e:
            logger.error(f"选择文件夹失败: {e}")
            return {'success': False, 'message': str(e)}


def start_flask():
    """启动Flask后端服务"""
    try:
        logger.info("🚀 启动Flask后端服务...")
        app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)
    except Exception as e:
        logger.error(f"Flask启动失败: {e}")
        sys.exit(1)


def main():
    """主函数"""
    # 在后台线程启动Flask
    flask_thread = threading.Thread(target=start_flask, daemon=True)
    flask_thread.start()
    
    # 等待Flask启动
    logger.info("⏳ 等待后端服务启动...")
    time.sleep(2)
    
    # 创建PyWebView窗口
    logger.info("🎨 创建应用窗口...")
    
    # 开发模式：连接到Vite开发服务器
    # 生产模式：使用Flask提供的静态文件
    # url = 'http://localhost:5173'  # Vite默认端口
    url = 'http://127.0.0.1:5000'  # 生产环境使用这个
    
    # 创建 API 实例
    api = API()
    
    window = webview.create_window(
        title='TronSync - 校园助手',
        url=url,
        width=1230,
        height=700,
        resizable=True,
        min_size=(800, 600),
        js_api=api  # 注入 API
    )
    
    logger.info("✅ 应用启动成功！")
    webview.start(debug=False)  # 关闭调试模式


if __name__ == '__main__':
    main()
