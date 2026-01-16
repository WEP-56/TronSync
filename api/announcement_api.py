import logging
import json
from bs4 import BeautifulSoup
from models.announcement import Announcement

logger = logging.getLogger(__name__)


class AnnouncementAPI:
    def __init__(self, session):
        self.session = session
        self.base_url = "https://tronclass.cityu.edu.mo"

    def get_bulletins(self, page_index: int = 1, page_size: int = 20):
        """
        获取指定页的公告列表
        :param page_index: 页码，默认为 1
        :param page_size: 每页数量，默认为 20
        :return: List[Announcement]
        """
        # 尝试直接调用API获取JSON数据
        # 通常这类系统会有API端点，先尝试常见的API路径
        api_url = f"{self.base_url}/api/course-bulletins"
        params = {
            "pageIndex": page_index,
            "pageSize": page_size,
            "type": "course"  # 科目公告
        }

        headers = {
            'Referer': 'https://tronclass.cityu.edu.mo/bulletin-list/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'X-Requested-With': 'XMLHttpRequest'
        }

        try:
            logger.info(f"正在请求第 {page_index} 页公告 (API)...")
            resp = self.session.get(api_url, params=params, headers=headers, timeout=10)

            if resp.status_code == 200:
                # 检查Content-Type判断是JSON还是HTML
                content_type = resp.headers.get('Content-Type', '').lower()
                
                if 'application/json' in content_type:
                    # 是JSON响应
                    try:
                        data = resp.json()
                        logger.info(f"API返回JSON数据类型: {type(data)}, 键: {list(data.keys()) if isinstance(data, dict) else 'N/A'}")
                        
                        # 如果返回的是JSON数据，直接解析
                        if isinstance(data, dict) and 'data' in data:
                            return self._parse_bulletins_json(data)
                        elif isinstance(data, dict) and 'list' in data:
                            # 尝试 data['list'] 结构
                            return self._parse_bulletins_json({'data': data['list']})
                        elif isinstance(data, dict) and 'bulletins' in data:
                            # 尝试 data['bulletins'] 结构
                            return self._parse_bulletins_json({'data': data['bulletins']})
                        elif isinstance(data, dict) and 'result' in data:
                            # 尝试 data['result'] 结构，可能包含list
                            result = data.get('result', {})
                            if isinstance(result, dict) and 'list' in result:
                                return self._parse_bulletins_json({'data': result['list']})
                            elif isinstance(result, list):
                                return self._parse_bulletins_json({'data': result})
                        elif isinstance(data, list):
                            return self._parse_bulletins_json_list(data)
                        else:
                            # 尝试直接解析dict中的所有可能字段
                            logger.warning(f"API返回的JSON格式不符合预期，尝试查找其他字段")
                            logger.debug(f"JSON内容预览: {str(data)[:500]}")
                            # 尝试直接解析整个dict作为公告列表（如果dict的values是列表）
                            for key, value in data.items():
                                if isinstance(value, list) and len(value) > 0:
                                    # 检查列表中的元素是否像公告对象
                                    if isinstance(value[0], dict) and 'title' in value[0]:
                                        logger.info(f"在字段 '{key}' 中找到公告列表")
                                        return self._parse_bulletins_json_list(value)
                            # 如果都失败了，尝试解析HTML
                            logger.warning("无法从JSON中提取公告，尝试解析HTML")
                            logger.info(f"完整的JSON结构（前1000字符）: {str(data)[:1000]}")
                            return self._parse_bulletins_html(resp.text)
                    except ValueError as e:
                        logger.warning(f"JSON解析失败: {e}，尝试解析HTML")
                        return self._parse_bulletins_html(resp.text)
                else:
                    # 是HTML响应，直接解析HTML
                    logger.info("API返回的是HTML，直接解析HTML")
                    return self._parse_bulletins_html(resp.text)
            else:
                logger.warning(f"API请求失败，状态码: {resp.status_code}，尝试HTML解析")
                # API失败，回退到HTML解析
                return self._get_bulletins_from_html(page_index)

        except Exception as e:
            logger.warning(f"API请求异常: {e}，尝试HTML解析", exc_info=True)
            # 异常时回退到HTML解析
            return self._get_bulletins_from_html(page_index)

    def _get_bulletins_from_html(self, page_index: int):
        """从HTML页面解析公告（备用方案）"""
        url = f"{self.base_url}/bulletin-list/"
        params = {"pageIndex": page_index}

        headers = {
            'Referer': 'https://tronclass.cityu.edu.mo/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36'
        }

        try:
            logger.info(f"正在请求第 {page_index} 页公告 (HTML)...")
            resp = self.session.get(url, params=params, headers=headers, timeout=10)

            if resp.status_code != 200:
                logger.error(f"请求失败，状态码: {resp.status_code}")
                return []

            return self._parse_bulletins_html(resp.text)

        except Exception as e:
            logger.error(f"获取公告网络异常: {e}", exc_info=True)
            return []

    def _parse_bulletins_json(self, data):
        """从JSON数据解析公告列表"""
        bulletins = []
        
        # 尝试不同的JSON结构
        if 'data' in data:
            items = data['data']
            if isinstance(items, list):
                items = items
            elif isinstance(items, dict) and 'list' in items:
                items = items['list']
            elif isinstance(items, dict) and 'bulletins' in items:
                items = items['bulletins']
            else:
                logger.warning(f"未知的JSON数据结构: {data.keys()}")
                return []
        else:
            items = data if isinstance(data, list) else []

        logger.info(f"从JSON找到 {len(items)} 条公告")

        for item in items:
            ann = Announcement()
            
            # 解析各个字段（根据实际API返回的字段名调整）
            ann.title = item.get('title', '')
            ann.course_name = item.get('course_name', '') or item.get('courseName', '')
            ann.created_at = item.get('created_at', '') or item.get('createdAt', '')
            ann.target = ', '.join(item.get('targets_name', [])) if isinstance(item.get('targets_name'), list) else item.get('targets_name', '')
            ann.content = item.get('content', '')
            
            bulletins.append(ann)

        return bulletins

    def _parse_bulletins_json_list(self, data_list):
        """从JSON列表解析公告"""
        bulletins = []
        logger.info(f"从JSON列表找到 {len(data_list)} 条公告")

        for item in data_list:
            ann = Announcement()
            ann.title = item.get('title', '')
            ann.course_name = item.get('course_name', '') or item.get('courseName', '')
            ann.created_at = item.get('created_at', '') or item.get('createdAt', '')
            ann.target = ', '.join(item.get('targets_name', [])) if isinstance(item.get('targets_name'), list) else item.get('targets_name', '')
            ann.content = item.get('content', '')
            bulletins.append(ann)

        return bulletins

    def _parse_bulletins_html(self, html):
        """从HTML解析公告（用于Angular渲染后的页面）"""
        soup = BeautifulSoup(html, "html.parser")

        # 1. 查找包含公告数据的script标签（可能包含JSON数据）
        script_tags = soup.find_all("script", type="application/json")
        for script in script_tags:
            script_id = script.get("id", "")
            if "bulletin" in script_id.lower():
                try:
                    data = json.loads(script.string)
                    logger.info("从script标签找到公告JSON数据")
                    return self._parse_bulletins_json(data)
                except Exception as e:
                    logger.debug(f"解析script标签JSON失败: {e}")
                    continue

        # 2. 查找实际渲染的公告内容
        # 注意：Angular渲染后的元素会有 ng-binding 类，说明有实际内容
        # 先尝试查找完整的容器
        container = soup.find("div", class_="bulletin-container")
        
        # 如果没找到完整容器，尝试直接查找所有公告项（可能是部分HTML）
        if not container:
            # 尝试查找部分匹配的容器
            container = soup.find("div", class_=lambda x: x and "bulletin" in x and "container" in x)
            if not container:
                # 尝试查找任何包含bulletin的div
                items = soup.find_all("div", class_="bulletin course-bulletin")
                if items:
                    logger.info(f"未找到容器，但直接找到 {len(items)} 条公告")
                else:
                    # 尝试查找任何包含bulletin的div（不要求完整class）
                    items = soup.find_all("div", class_=lambda x: x and "bulletin" in " ".join(x) if isinstance(x, list) else "bulletin" in str(x))
                    if items:
                        logger.info(f"找到 {len(items)} 个包含'bulletin'的div")
                    else:
                        logger.warning("未找到公告列表容器和公告项")
                        logger.debug(f"HTML内容预览（前500字符）: {html[:500]}")
                        return []
            else:
                items = container.find_all("div", class_="bulletin course-bulletin")
        else:
            # 3. 找到所有单条公告
            items = container.find_all("div", class_="bulletin course-bulletin")
        
        logger.info(f"从HTML找到 {len(items)} 条公告")

        bulletins = []
        for item in items:
            ann = Announcement()

            # --- 标题 ---
            # 查找有 ng-binding 类的span，说明已经被Angular渲染
            title_div = item.find("div", class_="bulletin-title")
            if title_div:
                span = title_div.find("span", class_="ng-binding")
                if span:
                    ann.title = span.get_text(strip=True)
                else:
                    # 如果没有ng-binding，尝试普通span
                    span = title_div.find("span")
                    if span:
                        text = span.get_text(strip=True)
                        if text:
                            ann.title = text

            # --- 元信息区域 (课程、时间、目标) ---
            info_div = item.find("div", class_="bulletin-update-info")
            if info_div:
                # 课程名称 - 查找有 ng-binding 类的span
                course_label = info_div.find("div", class_="course-name-label")
                if course_label:
                    span = course_label.find("span", class_="ng-binding")
                    if span:
                        ann.course_name = span.get_text(strip=True)
                    else:
                        # 尝试从title属性获取（tipsy属性）
                        span = course_label.find("span")
                        if span:
                            ann.course_name = span.get("title", "") or span.get_text(strip=True)

                # 时间 - 查找有 ng-binding 类且包含时间格式的span
                time_spans = info_div.find_all("span", class_="ng-binding")
                for span in time_spans:
                    text = span.get_text(strip=True)
                    # 时间格式通常是 2026.01.06 13:53 或类似
                    if text and '.' in text and ':' in text:
                        # 检查是否是时间格式（年份.月份.日期 时:分）
                        parts = text.split()
                        if len(parts) >= 2 and any(char.isdigit() for char in parts[0][:4]):
                            ann.created_at = text
                            break

                # 目标人群 - 查找有 ng-binding 类的span
                target_span = info_div.find("span", class_="group-target")
                if target_span:
                    inner_span = target_span.find("span", class_="ng-binding")
                    if inner_span:
                        ann.target = inner_span.get_text(strip=True)
                    else:
                        # 尝试从title属性获取
                        inner_span = target_span.find("span")
                        if inner_span:
                            ann.target = inner_span.get("title", "") or inner_span.get_text(strip=True)

            # --- 正文内容 ---
            # 查找有 ng-binding 类的simditor-viewer，说明内容已渲染
            content_div = item.find("div", class_="simditor-viewer")
            if content_div:
                # 检查是否有 ng-binding 类（说明内容已渲染）
                classes = content_div.get("class", [])
                if isinstance(classes, list) and "ng-binding" in classes:
                    # 获取HTML内容
                    ann.content = content_div.decode_contents()
                else:
                    # 如果没有ng-binding，尝试获取文本
                    content_text = content_div.get_text(strip=True)
                    if content_text:
                        ann.content = content_div.decode_contents()

            # 只有当至少有一个字段有值时才添加
            if ann.title or ann.course_name or ann.content:
                bulletins.append(ann)
                logger.debug(f"解析公告: {ann.title[:30] if ann.title else '无标题'}...")
            else:
                logger.debug("跳过空公告（可能是Angular模板）")

        if bulletins:
            logger.info(f"成功解析 {len(bulletins)} 条公告")
        else:
            logger.warning("未能解析出任何公告，请检查HTML结构")
            
        return bulletins