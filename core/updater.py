import os
import sys
import requests
import logging
import subprocess
import tempfile
import zipfile
import shutil
import time

logger = logging.getLogger(__name__)

# 默认 GitHub 仓库信息
DEFAULT_REPO_OWNER = "Jeza-Chen"
DEFAULT_REPO_NAME = "TronSync"

class Updater:
    def __init__(self, current_version, repo_owner=DEFAULT_REPO_OWNER, repo_name=DEFAULT_REPO_NAME):
        self.current_version = current_version
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.base_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"

    def check_for_updates(self):
        """检查 GitHub 最新发布版本"""
        try:
            logger.info(f"正在检查更新: {self.base_url}")
            headers = {
                "Accept": "application/vnd.github.v3+json",
                "User-Agent": "TronSync-Updater"
            }
            response = requests.get(self.base_url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                latest_version = data.get("tag_name", "").strip()
                
                # 简单版本比较：如果字符串不相等则认为有更新
                # 注意：实际场景可能需要更严谨的语义化版本比较
                if latest_version and latest_version != self.current_version:
                    # 查找发布产物中的 zip 包
                    assets = data.get("assets", [])
                    download_url = ""
                    asset_name = ""
                    
                    for asset in assets:
                        name = asset["name"].lower()
                        if name.endswith(".zip"):
                             download_url = asset["browser_download_url"]
                             asset_name = asset["name"]
                             break
                    
                    if not download_url:
                        # 如果没有 zip，尝试找 exe (虽然我们主要支持 zip)
                         for asset in assets:
                            name = asset["name"].lower()
                            if name.endswith(".exe"):
                                 download_url = asset["browser_download_url"]
                                 asset_name = asset["name"]
                                 break
                    
                    if not download_url:
                         logger.warning("未找到合适的发布资源 (.zip 或 .exe)")
                    
                    return {
                        "has_update": True,
                        "latest_version": latest_version,
                        "current_version": self.current_version,
                        "release_notes": data.get("body", ""),
                        "download_url": download_url,
                        "asset_name": asset_name,
                        "release_date": data.get("published_at", "")
                    }
                else:
                    return {"has_update": False, "message": "当前已是最新版本"}
            else:
                logger.error(f"检查更新失败: {response.status_code} - {response.text}")
                return {"error": f"检查更新失败: {response.status_code}"}
        except Exception as e:
            logger.error(f"检查更新异常: {e}")
            return {"error": str(e)}

    def perform_update(self, download_url):
        """执行更新流程"""
        try:
            # 1. 下载文件
            logger.info(f"开始下载更新: {download_url}")
            response = requests.get(download_url, stream=True)
            response.raise_for_status()
            
            # 确定临时文件路径
            filename = download_url.split("/")[-1]
            temp_dir = tempfile.mkdtemp()
            download_path = os.path.join(temp_dir, filename)
            
            with open(download_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            logger.info(f"更新包已下载至: {download_path}")
            
            # 2. 解压 (如果是 zip)
            extract_dir = os.path.join(temp_dir, "extracted")
            source_dir = extract_dir
            
            if filename.lower().endswith(".zip"):
                with zipfile.ZipFile(download_path, 'r') as zip_ref:
                    zip_ref.extractall(extract_dir)
                logger.info(f"Zip包已解压至: {extract_dir}")
                
                # 智能识别目录结构：如果解压后只有一个文件夹，则进入该文件夹
                items = os.listdir(extract_dir)
                if len(items) == 1 and os.path.isdir(os.path.join(extract_dir, items[0])):
                    source_dir = os.path.join(extract_dir, items[0])
                    logger.info(f"识别到嵌套目录，更新源路径调整为: {source_dir}")
            else:
                # 如果是 exe，创建一个目录放进去
                os.makedirs(extract_dir, exist_ok=True)
                shutil.copy(download_path, os.path.join(extract_dir, filename))
                source_dir = extract_dir

            # 3. 保护用户配置 (删除新包中的 config.json，防止覆盖)
            config_path_in_source = os.path.join(source_dir, "config.json")
            if os.path.exists(config_path_in_source):
                try:
                    os.remove(config_path_in_source)
                    logger.info("已从更新包中移除 config.json 以保留用户设置")
                except Exception as e:
                    logger.warning(f"移除更新包中的 config.json 失败: {e}")

            # 4. 创建更新脚本
            # 获取当前运行目录
            if getattr(sys, 'frozen', False):
                base_dir = os.path.dirname(sys.executable)
                exe_name = os.path.basename(sys.executable)
            else:
                # 开发环境，base_dir 是脚本所在目录
                base_dir = os.getcwd()
                exe_name = "TronSync.exe" # 假定名字
                logger.warning("开发环境执行更新，仅作演示")
                # return {"success": False, "message": "开发环境下无法执行真实更新"}

            bat_path = os.path.join(temp_dir, "update.bat")
            
            # 构造批处理命令
            # 逻辑：
            # 1. 等待主程序退出
            # 2. 删除旧的 _internal 文件夹 (如果是 PyInstaller 打包)
            # 3. 复制新文件覆盖
            # 4. 重启
            # 5. 清理临时目录
            
            bat_content = f"""@echo off
title TronSync Updater
echo Waiting for TronSync to close...
timeout /t 3 /nobreak > NUL

echo Removing old dependencies...
if exist "{base_dir}\\_internal" (
    rmdir /s /q "{base_dir}\\_internal"
)

echo Updating files...
xcopy /s /e /y "{source_dir}\\*" "{base_dir}\\"

echo Restarting application...
start "" "{os.path.join(base_dir, exe_name)}"

echo Cleaning up...
rd /s /q "{temp_dir}"
"""
            
            with open(bat_path, "w") as f:
                f.write(bat_content)
                
            logger.info(f"更新脚本已创建: {bat_path}")
            
            # 5. 启动脚本
            # 使用 shell=True 启动
            subprocess.Popen([bat_path], shell=True)
            
            return {"success": True, "message": "更新已启动，程序即将重启"}
            
        except Exception as e:
            logger.error(f"更新失败: {e}")
            return {"success": False, "message": str(e)}
