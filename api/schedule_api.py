import logging
from bs4 import BeautifulSoup
from models.schedule import CourseSchedule, WeekSchedule

logger = logging.getLogger(__name__)


class ScheduleAPI:
    def __init__(self, session):
        self.session = session
        self.base_url = "https://urp.cityu.edu.mo"
        # 正确的CAS认证跳转URL（从TronClass中找到的）
        self.cas_auth_url = "http://urp.cityu.edu.mo/sOfficeCas/CasToX2zForEau.aspx"
        self.schedule_page = "http://urp.cityu.edu.mo/ClassManagement/OuterLink.aspx?ToPage____OuterStudWeeklySchedule.aspx"
        
    def get_schedule(self, week_number: int = None):
        """
        获取课程表
        :param week_number: 周次，如果为None则获取当前周
        :return: WeekSchedule
        """
        try:
            logger.info(f"正在获取课程表（第 {week_number if week_number else '当前'} 周）...")
            
            # 第一步：通过CAS认证跳转到教务系统
            logger.info("正在进行CAS认证...")
            auth_success = self._authenticate_via_cas()
            
            if not auth_success:
                logger.error("CAS认证失败")
                return None
            
            logger.info("CAS认证成功")
            
            # 第二步：访问课程表页面
            logger.info("正在访问课程表页面...")
            schedule_url = "https://urp.cityu.edu.mo/ClassManagement/Pages/OuterStudWeeklySchedule.aspx"
            resp = self.session.get(schedule_url, timeout=10)
            
            if resp.status_code != 200:
                logger.error(f"访问课程表页面失败，状态码: {resp.status_code}")
                return None
            
            # 检查是否认证成功
            if "认证错误" in resp.text or "过期" in resp.text:
                logger.error("课程表页面认证失败")
                return None
            
            # 解析页面，提取隐藏字段
            soup = BeautifulSoup(resp.text, "html.parser")
            view_state = self._extract_viewstate(soup)
            
            # 第三步：如果需要提交表单获取特定周次
            if week_number:
                logger.info(f"正在提交表单获取第 {week_number} 周课程表...")
                schedule_html = self._submit_week_form(view_state, week_number)
                if schedule_html:
                    return self._parse_schedule_html(schedule_html, week_number)
            else:
                # 直接解析当前页面
                return self._parse_schedule_html(resp.text, week_number)
            
            return None
            
        except Exception as e:
            logger.error(f"获取课程表异常: {e}", exc_info=True)
            return None
    
    def _authenticate_via_cas(self):
        """通过CAS认证跳转到教务系统"""
        try:
            # 构造CAS认证URL
            import urllib.parse
            import re
            goto_url = urllib.parse.quote(self.schedule_page, safe='')
            
            cas_url = f"{self.cas_auth_url}?parm=other&goto={goto_url}&lang=zh-TW"
            
            logger.info(f"访问CAS认证URL...")
            logger.debug(f"CAS URL: {cas_url}")
            
            # 访问CAS认证页面，允许跳转
            resp = self.session.get(cas_url, timeout=15, allow_redirects=True)
            
            logger.info(f"认证响应状态码: {resp.status_code}")
            logger.info(f"最终URL: {resp.url}")
            
            # 检查是否成功跳转到教务系统
            if resp.status_code == 200 and 'urp.cityu.edu.mo' in resp.url:
                # 检查是否是JavaScript跳转页面
                if "window.location.href" in resp.text:
                    logger.info("检测到JavaScript跳转，提取跳转URL...")
                    
                    # 从JavaScript中提取跳转URL
                    # 格式: <script>window.location.href='URL';</script>
                    match = re.search(r"window\.location\.href\s*=\s*['\"]([^'\"]+)['\"]\s*;", resp.text)
                    if match:
                        redirect_url = match.group(1)
                        logger.info(f"找到跳转URL: {redirect_url}")
                        
                        # 跟随JavaScript跳转
                        resp2 = self.session.get(redirect_url, timeout=15, allow_redirects=True)
                        logger.info(f"跳转后状态码: {resp2.status_code}")
                        logger.info(f"跳转后URL: {resp2.url}")
                        
                        if resp2.status_code == 200:
                            # 检查是否包含错误信息
                            if "认证错误" not in resp2.text and "过期" not in resp2.text:
                                logger.info("✅ CAS认证成功（经过JavaScript跳转）")
                                return True
                            else:
                                logger.error("❌ JavaScript跳转后页面显示错误")
                                return False
                    else:
                        logger.error("❌ 无法从JavaScript中提取跳转URL")
                        return False
                
                # 直接检查页面内容
                if "认证错误" not in resp.text and "过期" not in resp.text:
                    logger.info("✅ CAS认证成功")
                    return True
                else:
                    logger.error("❌ CAS认证跳转成功但页面显示错误")
                    return False
            else:
                logger.error(f"❌ CAS认证失败，未跳转到教务系统")
                return False
                
        except Exception as e:
            logger.error(f"CAS认证异常: {e}", exc_info=True)
            return False
    
    def _extract_viewstate(self, soup):
        """提取ASP.NET ViewState等隐藏字段"""
        view_state = {}
        
        # 查找所有隐藏字段
        hidden_inputs = soup.find_all("input", {"type": "hidden"})
        for inp in hidden_inputs:
            name = inp.get("name")
            value = inp.get("value", "")
            if name:
                view_state[name] = value
                if name in ["__VIEWSTATE", "__VIEWSTATEGENERATOR", "__EVENTVALIDATION"]:
                    logger.debug(f"找到 {name}: {value[:50]}...")
        
        return view_state if view_state else None
    
    def _submit_week_form(self, view_state, week_number):
        """提交表单切换周次"""
        try:
            # 构造POST数据
            payload = view_state.copy()
            
            # 添加周次选择（具体字段名需要根据实际页面调整）
            payload['__EVENTTARGET'] = ''  # 可能需要调整
            payload['__EVENTARGUMENT'] = ''
            # 这里需要根据实际表单字段名添加周次参数
            # payload['ctl00$ContentPlaceHolder1$ddlWeek'] = str(week_number)
            
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Referer': self.schedule_url,
                'Origin': self.base_url,
            }
            
            logger.info("正在提交表单...")
            resp = self.session.post(
                self.schedule_url,
                data=payload,
                headers=headers,
                timeout=10
            )
            
            if resp.status_code == 200:
                logger.info("表单提交成功")
                return resp.text
            else:
                logger.error(f"表单提交失败，状态码: {resp.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"提交表单异常: {e}", exc_info=True)
            return None
    
    def _parse_schedule_html(self, html, week_number=None):
        """解析课程表HTML"""
        try:
            soup = BeautifulSoup(html, "html.parser")
                
            # 创建课程表对象
            schedule = WeekSchedule(week_number=week_number or 0)
                
            # 查找包含TopHeader的table（课程表）
            table = None
            tables = soup.find_all("table")
            for t in tables:
                if t.find("th", class_="TopHeader"):
                    table = t
                    break
                
            if not table:
                logger.warning("未找到课程表table")
                return schedule
                
            logger.info("找到课程表table，开始解析...")
                
            # 解析表头（星期）
            headers = table.find_all("th", class_="TopHeader")
            weekday_map = {}  # 列索引 -> 星期几
                
            for idx, th in enumerate(headers):
                text = th.get_text(strip=True)
                if "星期日" in text:
                    weekday_map[idx] = 7
                elif "星期一" in text:
                    weekday_map[idx] = 1
                elif "星期二" in text:
                    weekday_map[idx] = 2
                elif "星期三" in text:
                    weekday_map[idx] = 3
                elif "星期四" in text:
                    weekday_map[idx] = 4
                elif "星期五" in text:
                    weekday_map[idx] = 5
                elif "星期六" in text:
                    weekday_map[idx] = 6
                
            logger.info(f"解析到 {len(weekday_map)} 天的课程")
                
            # 解析课程单元格
            used_cells = table.find_all("td", class_="Used")
            logger.info(f"找到 {len(used_cells)} 个课程单元格")
                
            for cell in used_cells:
                try:
                    div = cell.find("div")
                    if not div:
                        continue
                        
                    span = div.find("span")
                    if not span:
                        continue
                        
                    # 提取课程信息（格式: 课程名<br />教师<br />教室）
                    html_content = str(span)
                    parts = html_content.split("<br/>") if "<br/>" in html_content else html_content.split("<br />")
                        
                    if len(parts) < 3:
                        continue
                        
                    # 提取文本
                    from bs4 import BeautifulSoup as BS
                    course_name = BS(parts[0], "html.parser").get_text(strip=True)
                    teacher = BS(parts[1], "html.parser").get_text(strip=True)
                    classroom = BS(parts[2], "html.parser").get_text(strip=True)
                        
                    if not course_name:
                        continue
                        
                    # 确定星期几
                    parent_tr = cell.find_parent("tr")
                    if not parent_tr:
                        continue
                        
                    all_tds = parent_tr.find_all("td")
                    cell_index = next((i for i, td in enumerate(all_tds) if td == cell), None)
                        
                    if cell_index is None:
                        continue
                        
                    week_day = weekday_map.get(cell_index, 0)
                    if week_day == 0:
                        continue
                        
                    # 获取时间
                    time_th = parent_tr.find("th", class_="LeftHeader")
                    time_range = time_th.get_text(strip=True) if time_th else ""
                        
                    start_time = ""
                    end_time = ""
                    if " - " in time_range:
                        times = time_range.split(" - ")
                        if len(times) == 2:
                            start_time = times[0].strip()
                            end_time = times[1].strip()
                        
                    # 创建课程对象
                    course_schedule = CourseSchedule(
                        course_name=course_name,
                        teacher=teacher,
                        classroom=classroom,
                        week_day=week_day,
                        start_time=start_time,
                        end_time=end_time
                    )
                        
                    schedule.schedules.append(course_schedule)
                    logger.debug(f"解析课程: {course_name} - {teacher} - 星期{week_day}")
                        
                except Exception as e:
                    logger.error(f"解析课程单元格失败: {e}", exc_info=True)
                    continue
                
            logger.info(f"成功解析 {len(schedule.schedules)} 节课程")
            return schedule
                
        except Exception as e:
            logger.error(f"解析课程表HTML异常: {e}", exc_info=True)
            return WeekSchedule(week_number=week_number or 0)
    
    def login_urp_system(self, username, password):
        """
        登录教务系统（如果需要单独登录）
        :param username: 用户名
        :param password: 密码
        :return: bool
        """
        try:
            logger.info("正在登录教务系统...")
            
            # 访问登录页
            login_url = f"{self.base_url}/login"  # 需要确认实际登录URL
            resp = self.session.get(login_url, timeout=10)
            
            if resp.status_code != 200:
                logger.error(f"访问登录页失败，状态码: {resp.status_code}")
                return False
            
            # 解析登录页，提取隐藏字段
            soup = BeautifulSoup(resp.text, "html.parser")
            view_state = self._extract_viewstate(soup)
            
            # 构造登录数据
            payload = view_state.copy() if view_state else {}
            payload['username'] = username  # 需要确认实际字段名
            payload['password'] = password
            
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Referer': login_url,
                'Origin': self.base_url,
            }
            
            # 提交登录
            logger.info("正在提交登录信息...")
            login_resp = self.session.post(
                login_url,
                data=payload,
                headers=headers,
                timeout=10,
                allow_redirects=True
            )
            
            # 检查登录结果
            if login_resp.status_code == 200 and "login" not in login_resp.url.lower():
                logger.info("✅ 教务系统登录成功")
                return True
            else:
                logger.error("❌ 教务系统登录失败")
                return False
                
        except Exception as e:
            logger.error(f"登录教务系统异常: {e}", exc_info=True)
            return False
