import json
import os

CONFIG_FILE = "config.json"

def load_config():
    """读取配置文件，如果不存在返回默认空配置"""
    if not os.path.exists(CONFIG_FILE):
        return {
            "username": "", 
            "password": "",
            "remember_password": False,
            "auto_login": False
        }
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            config = json.load(f)
            # 确保包含所有必要字段
            if 'remember_password' not in config:
                config['remember_password'] = False
            if 'auto_login' not in config:
                config['auto_login'] = False
            return config
    except Exception as e:
        print(f"读取配置文件失败: {e}")
        return {
            "username": "", 
            "password": "",
            "remember_password": False,
            "auto_login": False
        }

def save_config(config):
    """保存配置到 JSON（接受完整的配置字典）"""
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        print(f"✅ 配置已保存: remember_password={config.get('remember_password')}, auto_login={config.get('auto_login')}")
    except Exception as e:
        print(f"保存配置文件失败: {e}")

# 保留旧的函数签名以兼容旧代码
def save_credentials(username, password):
    """保存账号密码（兼容旧代码）"""
    config = load_config()
    config['username'] = username
    config['password'] = password
    save_config(config)