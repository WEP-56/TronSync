import logging
import json
from bs4 import BeautifulSoup
from models.course import Course

logger = logging.getLogger(__name__)


class CourseAPI:
    def __init__(self, session):
        self.session = session
        self.base_url = "https://tronclass.cityu.edu.mo"

    def get_courses(self, page_index: int = 1):
        """
        获取课程列表
        :param page_index: 页码，默认为 1
        :return: List[Course]
        """
        # 尝试通过API获取JSON数据
        courses = self._get_courses_from_api(page_index)
        if courses:
            return courses
        
        # API失败时回退到HTML解析
        logger.info("API方式失败，尝试HTML解析")
        return self._get_courses_from_html(page_index)

    def _get_courses_from_api(self, page_index: int):
        """尝试通过API获取课程JSON数据"""
        # 常见的课程API端点（按优先级排序）
        api_endpoints = [
            f"{self.base_url}/api/my-courses",  # 实际发现的API端点
            f"{self.base_url}/api/users/courses",
            f"{self.base_url}/api/user/courses",
            f"{self.base_url}/api/course/list",
            f"{self.base_url}/api/courses",
        ]
        
        params = {
            "pageIndex": page_index,
            "pageSize": 20,
        }
        
        headers = {
            'Referer': 'https://tronclass.cityu.edu.mo/user/courses',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'X-Requested-With': 'XMLHttpRequest'
        }
        
        for api_url in api_endpoints:
            try:
                logger.info(f"尝试API: {api_url}")
                resp = self.session.get(api_url, params=params, headers=headers, timeout=10)
                
                if resp.status_code == 200:
                    content_type = resp.headers.get('Content-Type', '').lower()
                    
                    if 'application/json' in content_type:
                        try:
                            data = resp.json()
                            logger.info(f"API返回JSON，键: {list(data.keys()) if isinstance(data, dict) else 'list'}")
                            
                            # 尝试解析不同的JSON结构
                            courses = self._try_parse_json_courses(data)
                            if courses:
                                logger.info(f"通过API成功获取 {len(courses)} 门课程")
                                return courses
                        except Exception as e:
                            logger.debug(f"JSON解析失败: {e}")
                            continue
            except Exception as e:
                logger.debug(f"API请求失败 {api_url}: {e}")
                continue
        
        logger.info("所有API端点都失败")
        return []
    
    def _try_parse_json_courses(self, data):
        """尝试从不同结构的JSON中解析课程列表"""
        # 尝试多种可能的JSON结构
        possible_paths = [
            ['data', 'courses'],
            ['data', 'list'],
            ['result', 'courses'],
            ['result', 'list'],
            ['courses'],
            ['list'],
            ['data'],
        ]
        
        for path in possible_paths:
            try:
                current = data
                for key in path:
                    if isinstance(current, dict) and key in current:
                        current = current[key]
                    else:
                        break
                else:
                    # 如果成功遍历完path
                    if isinstance(current, list) and len(current) > 0:
                        # 检查是否像课程列表
                        if isinstance(current[0], dict) and ('name' in current[0] or 'display_name' in current[0]):
                            logger.info(f"在路径 {' -> '.join(path)} 找到课程列表")
                            return self._parse_courses_json_list(current)
            except Exception as e:
                logger.debug(f"尝试路径 {path} 失败: {e}")
                continue
        
        return []

    def _get_courses_from_html(self, page_index: int):
        """从HTML页面解析课程"""
        # 注意：URL中的 #/ 是前端路由，requests请求时不需要包含
        # 实际请求的URL应该是: /user/courses?pageIndex=1
        url = f"{self.base_url}/user/courses"
        params = {"pageIndex": page_index}

        headers = {
            'Referer': 'https://tronclass.cityu.edu.mo/user/courses',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36'
        }

        try:
            logger.info(f"正在请求第 {page_index} 页课程...")
            logger.debug(f"请求URL: {url}, 参数: {params}")
            resp = self.session.get(url, params=params, headers=headers, timeout=10)

            if resp.status_code != 200:
                logger.error(f"请求失败，状态码: {resp.status_code}")
                return []

            # 调试：检查HTML中是否包含课程数据
            html_text = resp.text
            # 统计data-course-id的数量
            course_id_count = html_text.count('data-course-id=')
            logger.info(f"HTML中包含 {course_id_count} 个data-course-id属性")
            
            # 检查是否有ng-binding类（说明已渲染）
            ng_binding_count = html_text.count('ng-binding')
            logger.info(f"HTML中包含 {ng_binding_count} 个ng-binding类（已渲染的元素）")
            
            # 检查是否包含Angular模板语法（说明未渲染）
            if '[[instructor.name]]' in html_text or 'ng-repeat="course in' in html_text:
                logger.warning("⚠️  HTML包含Angular模板语法，说明页面未被渲染，需要通过API获取数据")
                logger.info("尝试查找HTML中嵌入的JSON数据...")
                
                # 尝试从HTML中提取嵌入的JSON数据
                courses = self._extract_json_from_html(html_text)
                if courses:
                    return courses
                
                logger.error("无法从HTML中提取课程数据，请使用浏览器开发者工具查看网络请求，找到正确的API端点")
                return []
            
            return self._parse_courses_html(html_text)

        except Exception as e:
            logger.error(f"获取课程网络异常: {e}", exc_info=True)
            return []
    
    def _extract_json_from_html(self, html_text):
        """尝试从HTML中提取嵌入的JSON数据"""
        import re
        import json
        
        # 查找<script>标签中的JSON数据
        script_patterns = [
            r'var\s+courses\s*=\s*(\[.*?\]);',
            r'window\.courses\s*=\s*(\[.*?\]);',
            r'"courses"\s*:\s*(\[.*?\])',
        ]
        
        for pattern in script_patterns:
            matches = re.findall(pattern, html_text, re.DOTALL)
            for match in matches:
                try:
                    data = json.loads(match)
                    if isinstance(data, list) and len(data) > 0:
                        logger.info(f"从<script>标签中提取到 {len(data)} 门课程")
                        return self._parse_courses_json_list(data)
                except:
                    continue
        
        return []

    def _parse_courses_json_list(self, courses_list):
        """从JSON列表解析课程"""
        courses = []
        logger.info(f"从JSON找到 {len(courses_list)} 门课程")

        for item in courses_list:
            course = Course()
            course.course_id = str(item.get('id', ''))
            course.name = item.get('display_name', '') or item.get('name', '')
            course.course_code = item.get('course_code', '')
            
            # 解析学期信息（可能是字符串或字典）
            semester = item.get('semester', '')
            if isinstance(semester, dict):
                # 从字典中提取学期代码或名称
                course.semester = semester.get('code', '') or semester.get('name', '') or semester.get('real_name', '')
            else:
                course.semester = item.get('semester_name', '') or str(semester)
            
            course.department = item.get('department', {}).get('name', '') if isinstance(item.get('department'), dict) else ''
            course.grade = item.get('grade', {}).get('name', '') if isinstance(item.get('grade'), dict) else ''
            course.klass = item.get('klass', {}).get('name', '') if isinstance(item.get('klass'), dict) else ''
            course.start_date = item.get('start_date', '')
            course.end_date = item.get('end_date', '')
            course.teaching_class = item.get('course_attributes', {}).get('teaching_class_name', '') if isinstance(item.get('course_attributes'), dict) else ''
            course.compulsory = "必修" if item.get('compulsory') is True else ("選修" if item.get('compulsory') is False else "")
            course.credit = str(item.get('credit', ''))
            course.cover_url = item.get('cover_url', '') or item.get('cover', '')
            course.course_url = item.get('course_url', '') or f"/course/{course.course_id}/content"
            
            # 解析教师列表
            instructors = item.get('instructors', [])
            if isinstance(instructors, list):
                course.instructors = [inst.get('name', '') or inst.get('display_name', '') for inst in instructors if isinstance(inst, dict)]
            
            courses.append(course)

        return courses

    def _parse_courses_html(self, html):
        """从HTML解析课程（用于Angular渲染后的页面）"""
        soup = BeautifulSoup(html, "html.parser")

        # 直接查找所有课程的li元素（每门课程都在一个<li class="course">中）
        course_items = soup.find_all("li", class_="course")
        logger.info(f"找到 {len(course_items)} 个课程li元素")
        
        if not course_items:
            logger.warning("未找到课程内容")
            return []

        courses = []
        for idx, course_li in enumerate(course_items, 1):
            try:
                course = Course()

                # 获取课程ID（从li元素的data-course-id属性）
                course.course_id = course_li.get("data-course-id", "")

                # 查找course-content div（包含主要信息）
                content_div = course_li.find("div", class_="course-content")
                if not content_div:
                    logger.warning(f"第 {idx} 个课程没有course-content，跳过")
                    continue

                # --- 课程名称和链接 ---
                course_name_span = content_div.find("span", class_="course-name")
                if course_name_span:
                    # 从a标签获取名称和链接
                    a_tag = course_name_span.find("a", class_="ng-binding")
                    if a_tag:
                        course.name = a_tag.get_text(strip=True)
                        course.course_url = a_tag.get("href", "")
                    else:
                        # 如果没有a标签，尝试从title或text获取
                        course.name = course_name_span.get("title", "") or course_name_span.get_text(strip=True)

                # --- 科目代码 ---
                code_row = content_div.find("div", class_="course-code-row")
                if code_row:
                    code_span = code_row.find("span", class_="ng-binding")
                    if code_span:
                        course.course_code = code_span.get_text(strip=True)

                # --- 学期信息 ---
                # 学期在right div中的course-academic-year-semester
                right_div = content_div.find("div", class_="right")
                if right_div:
                    semester_div = right_div.find("div", class_="course-academic-year-semester")
                    if semester_div:
                        semester_span = semester_div.find("span", class_="ng-binding")
                        if semester_span:
                            course.semester = semester_span.get_text(strip=True)

                # --- 系级、年级、班级、开课日期 ---
                summarize = content_div.find("div", class_="course-summarize")
                if summarize:
                    # 查找所有course-summarize-item
                    items_list = summarize.find_all("div", class_="course-summarize-item")
                    
                    # 处理非日期的项（系级、年级、班级）
                    non_date_items = []
                    for summarize_item in items_list:
                        # 检查是否是course-cycle（开课日期）
                        if "course-cycle" in summarize_item.get("class", []):
                            # 解析开课日期
                            # 结构: <span>開課: </span><span>2026-01-05</span> <span>－ 科目結束日期: </span><span>2026-05-02</span>
                            date_spans = summarize_item.find_all("span", class_="ng-binding")
                            if len(date_spans) >= 1:
                                course.start_date = date_spans[0].get_text(strip=True)
                            if len(date_spans) >= 2:
                                course.end_date = date_spans[1].get_text(strip=True)
                        else:
                            # 非日期项：系级、年级、班级
                            span = summarize_item.find("span", class_="ng-binding")
                            if span:
                                non_date_items.append(span.get_text(strip=True))
                    
                    # 按顺序分配到系级、年级、班级
                    if len(non_date_items) >= 1:
                        course.department = non_date_items[0]
                    if len(non_date_items) >= 2:
                        course.grade = non_date_items[1]
                    if len(non_date_items) >= 3:
                        course.klass = non_date_items[2]

                # --- 课程详情（授课班级、必选修别、学分数、授课教师） ---
                detail = content_div.find("div", class_="course-detail")
                if detail:
                    detail_row = detail.find("div", class_="detail-row")
                    if detail_row:
                        # 授课班级
                        teaching_class_div = detail_row.find("div", class_="teaching-class-name")
                        if teaching_class_div:
                            teaching_span = teaching_class_div.find("span", class_="ng-binding")
                            if teaching_span:
                                course.teaching_class = teaching_span.get_text(strip=True)

                        # 必选修别
                        compulsory_div = detail_row.find("div", class_="compulsory")
                        if compulsory_div:
                            # 查找ng-switch-when的span（必修或選修）
                            compulsory_span = compulsory_div.find("span", class_=lambda x: x and "ng-scope" in x)
                            if compulsory_span:
                                text = compulsory_span.get_text(strip=True)
                                if text in ["必修", "選修"]:
                                    course.compulsory = text

                        # 学分数
                        credit_div = detail_row.find("div", class_="credit")
                        if credit_div:
                            credit_span = credit_div.find("span", class_="ng-binding")
                            if credit_span:
                                course.credit = credit_span.get_text(strip=True)

                        # 授课教师
                        instructor_div = detail_row.find("div", class_="instructor")
                        if instructor_div:
                            # 查找所有user-avatar div
                            avatars = instructor_div.find_all("div", class_="user-avatar")
                            for avatar in avatars:
                                # 查找avatar16 div，它有tipsy-literal或original-title属性
                                avatar16 = avatar.find("div", class_="avatar16")
                                if avatar16:
                                    teacher_name = avatar16.get("tipsy-literal") or avatar16.get("original-title")
                                    if teacher_name:
                                        course.instructors.append(teacher_name)

                # --- 课程封面 ---
                # 封面在同一个li下的course-cover div中
                cover_div = course_li.find("div", class_="course-cover")
                if cover_div:
                    img = cover_div.find("img")
                    if img:
                        course.cover_url = img.get("src", "") or img.get("ng-src", "")

                # 只有当至少有一个字段有值时才添加
                if course.name or course.course_id:
                    courses.append(course)
                    logger.debug(f"[{idx}] 解析课程: {course.name}")
                else:
                    logger.warning(f"第 {idx} 个课程解析失败，name和course_id都为空")

            except Exception as e:
                logger.error(f"解析第 {idx} 个课程时出错: {e}", exc_info=True)
                continue

        if courses:
            logger.info(f"成功解析 {len(courses)} 门课程")
        else:
            logger.warning("未能解析出任何课程，请检查HTML结构")

        return courses