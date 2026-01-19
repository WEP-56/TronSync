"""
TronSync启动器
使用PyWebView创建桌面应用窗口，Flask作为后端服务
"""
import webview
import threading
import time
import sys
import os
import json
import logging
from tkinter import filedialog
import tkinter as tk
import ctypes
from ctypes import windll

from app import app

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Windows 常量
WM_NCLBUTTONDOWN = 0x00A1
HTCAPTION = 2

# 缩放方向映射 (HitTest Values)
RESIZE_MAP = {
    'left': 10,       # HTLEFT
    'right': 11,      # HTRIGHT
    'top': 12,        # HTTOP
    'top-left': 13,   # HTTOPLEFT
    'top-right': 14,  # HTTOPRIGHT
    'bottom': 15,     # HTBOTTOM
    'bottom-left': 16,# HTBOTTOMLEFT
    'bottom-right': 17# HTBOTTOMRIGHT
}

class API:
    """PyWebView API 类，用于前端调用桌面功能"""
    
    def __init__(self):
        self._window = None

    def set_window(self, window):
        self._window = window

    def minimize(self):
        """最小化窗口"""
        if self._window:
            self._window.minimize()

    def maximize(self):
        """最大化/还原窗口"""
        if self._window:
            self._window.toggle_fullscreen()

    def close(self):
        """关闭窗口"""
        if self._window:
            self._window.destroy()

    def start_drag(self):
        """开始拖拽窗口 (已废弃，改用前端 CSS drag)"""
        pass

    def start_resize(self, direction):
        """开始缩放窗口 (已废弃，改用前端模拟)"""
        pass
    
    def get_window_geometry(self):
        """获取窗口位置和大小"""
        if self._window:
            return {
                'x': self._window.x,
                'y': self._window.y,
                'width': self._window.width,
                'height': self._window.height
            }
        return None

    def set_window_geometry(self, x, y, width, height):
        """设置窗口位置和大小"""
        if self._window:
            try:
                self._window.move(int(x), int(y))
                self._window.resize(int(width), int(height))
            except Exception as e:
                logger.error(f"设置窗口几何信息失败: {e}")
    
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

    def load_config(self):
        """加载配置文件"""
        try:
            config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                return {'success': True, 'data': config}
            return {'success': False, 'message': 'Config file not found'}
        except Exception as e:
            logger.error(f"加载配置文件失败: {e}")
            return {'success': False, 'message': str(e)}

    def save_config(self, config_data):
        """保存配置文件"""
        try:
            config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=4, ensure_ascii=False)
            return {'success': True}
        except Exception as e:
            logger.error(f"保存配置文件失败: {e}")
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
        frameless=True,
        easy_drag=False,
        js_api=api  # 注入 API
    )
    
    api.set_window(window)
    
    logger.info("✅ 应用启动成功！")
    webview.start(debug=False)  # 关闭调试模式

if __name__ == '__main__':
    main()
