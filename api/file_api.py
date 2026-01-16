from core.session_manager import SessionManager
from models.user_profile import UserProfile
from bs4 import BeautifulSoup
import json
import re
import logging

logger = logging.getLogger(__name__)


class FileAPI:
    def __init__(self, session):
        self.session = session
        self.base_url = "https://tronclass.cityu.edu.mo"

    def get_folder_info(self, folder_id):
        """
        获取文件夹信息
        Args:
            folder_id: 文件夹ID
        Returns:
            dict: 文件夹信息
        """
        try:
            url = f"{self.base_url}/api/uploads/{folder_id}"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "id": data.get("id"),
                    "name": data.get("name"),
                    "parent_id": data.get("parent_id", 0)
                }
        except Exception as e:
            logger.error(f"获取文件夹信息失败: {e}")
        
        return None

    def get_files(self, page=1, page_size=20, parent_id=0):
        """
        获取用户文件列表
        Args:
            page: 页码
            page_size: 每页数量
            parent_id: 父文件夹ID，0表示根目录
        Returns:
            dict: 包含文件列表和路径信息
        """
        try:
            # 构造查询参数 - 包含所有文件类型
            conditions = {
                "keyword": "",
                "includeSlides": False,
                "limitTypes": ["file", "video", "document", "image", "audio", "scorm", "evercam", "swf", "wmpkg", "link", "folder"],
                "fileType": "all",
                "parentId": parent_id,
                "sourceType": "MyResourcesFile",
                "sortPredicate": "created_at",
                "reverse": True,
                "no-intercept": True
            }
            
            params = {
                "conditions": json.dumps(conditions),
                "page": page,
                "page_size": page_size
            }
            
            url = f"{self.base_url}/api/user/resources"
            
            logger.info(f"正在请求文件列表: {url}")
            logger.info(f"请求参数: page={page}, page_size={page_size}, parent_id={parent_id}")
            
            response = self.session.get(url, params=params, timeout=15)
            
            logger.info(f"响应状态码: {response.status_code}")
            
            if response.status_code != 200:
                logger.error(f"请求失败，状态码: {response.status_code}")
                logger.error(f"响应内容: {response.text[:500]}")
                return {
                    "files": [],
                    "breadcrumb": [{"id": 0, "name": "根目录"}],
                    "parent_id": parent_id,
                    "total": 0,
                    "page": 1,
                    "pages": 1
                }
            
            # 尝试解析JSON
            try:
                data = response.json()
                logger.info(f"成功解析JSON响应")
                logger.debug(f"响应数据结构: {list(data.keys()) if isinstance(data, dict) else type(data)}")
            except json.JSONDecodeError as e:
                logger.error(f"JSON解析失败: {e}")
                logger.error(f"响应内容: {response.text[:500]}")
                return {
                    "files": [],
                    "breadcrumb": [{"id": 0, "name": "根目录"}],
                    "parent_id": parent_id,
                    "total": 0,
                    "page": 1,
                    "pages": 1
                }
            
            # 检查响应数据结构
            if isinstance(data, dict):
                # 实际的数据结构: {"page": 1, "pages": 2, "total": 23, "uploads": [...]}
                if "uploads" in data:
                    items = data["uploads"]
                    total = data.get("total", len(items))
                    logger.info(f"从 uploads 字段获取到 {len(items)} 个项目，总共 {total} 个")
                elif "data" in data:
                    items = data["data"]
                    logger.info(f"从 data 字段获取到 {len(items)} 个项目")
                else:
                    logger.warning(f"响应中没有 uploads 或 data 字段，可用字段: {list(data.keys())}")
                    return {
                        "files": [],
                        "breadcrumb": [{"id": 0, "name": "根目录"}],
                        "parent_id": parent_id,
                        "total": 0,
                        "page": 1,
                        "pages": 1
                    }
            elif isinstance(data, list):
                # 直接返回列表
                items = data
                logger.info(f"直接获取到列表，共 {len(items)} 个项目")
            else:
                logger.error(f"未知的响应数据类型: {type(data)}")
                return {
                    "files": [],
                    "breadcrumb": [{"id": 0, "name": "根目录"}],
                    "parent_id": parent_id,
                    "total": 0,
                    "page": 1,
                    "pages": 1
                }
            
            # 解析文件列表
            files = []
            for item in items:
                # 判断是否是文件夹
                is_folder = item.get("is_folder", False)
                item_type = "folder" if is_folder else item.get("type", "file")
                
                file_info = {
                    "id": item.get("id"),
                    "name": item.get("name", "未命名"),
                    "type": item_type,  # folder, document, video, image, file 等
                    "size": item.get("size", 0),
                    "created_at": item.get("created_at", ""),
                    "updated_at": item.get("updated_at", ""),
                    "owner_id": item.get("owner_id"),
                    "reference_count": item.get("reference_count", 0),
                    "allow_download": item.get("allow_download", True),
                    "status": item.get("status", "ready"),
                    "is_folder": is_folder
                }
                files.append(file_info)
                logger.debug(f"解析文件: {file_info['name']} (类型: {file_info['type']}, 是否文件夹: {is_folder})")
            
            logger.info(f"✅ 成功获取 {len(files)} 个文件/文件夹")
            
            # 构建面包屑路径
            breadcrumb = self._build_breadcrumb(parent_id)
            
            return {
                "files": files,
                "breadcrumb": breadcrumb,
                "parent_id": parent_id,
                "total": data.get("total", len(files)),
                "page": page,
                "pages": data.get("pages", 1)
            }
            
        except Exception as e:
            logger.error(f"获取文件列表异常: {str(e)}", exc_info=True)
            return {
                "files": [],
                "breadcrumb": [{"id": 0, "name": "根目录"}],
                "parent_id": 0,
                "total": 0,
                "page": 1,
                "pages": 1
            }

    def _build_breadcrumb(self, folder_id):
        """
        构建面包屑路径（简化版本）
        Args:
            folder_id: 当前文件夹ID
        Returns:
            list: 面包屑路径列表
        """
        # 简化版本：只显示根目录和当前文件夹
        # TODO: 后续可以通过缓存文件夹路径来实现完整的面包屑
        breadcrumb = [{"id": 0, "name": "根目录"}]
        
        if folder_id != 0:
            # 尝试获取当前文件夹信息
            folder_info = self.get_folder_info(folder_id)
            if folder_info:
                breadcrumb.append({
                    "id": folder_info["id"],
                    "name": folder_info["name"]
                })
                logger.info(f"面包屑: 根目录 > {folder_info['name']}")
            else:
                # 如果获取失败，使用占位符
                breadcrumb.append({
                    "id": folder_id,
                    "name": f"文件夹 {folder_id}"
                })
                logger.warning(f"无法获取文件夹 {folder_id} 的信息，使用占位符")
        
        return breadcrumb