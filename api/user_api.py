import logging
from bs4 import BeautifulSoup
from models.user_profile import UserProfile

logger = logging.getLogger(__name__)


class UserAPI:
    def __init__(self, session):
        self.session = session
        self.base_url = "https://tronclass.cityu.edu.mo"

    def get_profile(self):
        """获取并解析用户个人资料"""
        url = f"{self.base_url}/user/settings#/"
        headers = {
            'Referer': 'https://tronclass.cityu.edu.mo/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36'
        }

        try:
            logger.info(f"正在请求个人详情页: {url}")
            resp = self.session.get(url, headers=headers, timeout=10)

            if resp.status_code != 200:
                logger.error(f"请求失败，状态码: {resp.status_code}")
                return None

            return self._parse_profile(resp.text)

        except Exception as e:
            logger.error(f"获取个人信息网络异常: {e}", exc_info=True)
        return None

    def _parse_profile(self, html):
        soup = BeautifulSoup(html, "html.parser")
        profile = UserProfile()

        # ==========================================
        # 1. 获取头像
        # ==========================================
        avatar_tag = soup.find("root-scope-variable", attrs={"name": "avatarBigUrl"})
        if avatar_tag:
            profile.avatar_url = avatar_tag.get("value", "")
            logger.info(f"✅ 成功获取头像 URL")

        # ==========================================
        # 2. 获取姓名（从隐藏input或root-scope-variable获取）
        # ==========================================
        # 方法1: 从隐藏input获取
        name_input = soup.find("input", id="myName")
        if name_input:
            profile.name_cn = name_input.get("value", "")
            logger.info(f"✅ 从隐藏input获取姓名: {profile.name_cn}")
        else:
            # 方法2: 从root-scope-variable获取
            name_var = soup.find("root-scope-variable", attrs={"name": "currentUserName"})
            if name_var:
                profile.name_cn = name_var.get("value", "")
                logger.info(f"✅ 从root-scope-variable获取姓名: {profile.name_cn}")

        # ==========================================
        # 3. 获取英文姓名（从ng-init属性解析）
        # ==========================================
        # 查找包含myNickname的ng-init属性
        user_settings = soup.find("div", class_="user-settings")
        if user_settings:
            ng_init = user_settings.get("ng-init", "")
            if "myNickname" in ng_init:
                # 解析 ng-init="myNickname='PAN SHIDING';"
                import re
                match = re.search(r"myNickname=['\"]([^'\"]+)['\"]", ng_init)
                if match:
                    profile.name_en = match.group(1)
                    logger.info(f"✅ 从ng-init获取英文姓名: {profile.name_en}")

        # ==========================================
        # 4. 获取其他字段
        # ==========================================
        # 方法1: 通过特定的class直接查找（更可靠）
        
        # 获取帳號 (从 class="row collapse user_no")
        user_no_row = soup.find("div", class_="row collapse user_no")
        if user_no_row:
            value_div = user_no_row.find("div", class_="value")
            if value_div:
                span = value_div.find("span")
                if span:
                    profile.account = span.get_text(strip=True)
                    logger.info(f"✅ 获取帳號: {profile.account}")
        
        # 获取平台角色 (从 class="row collapse role")
        role_row = soup.find("div", class_="row collapse role")
        if role_row:
            value_div = role_row.find("div", class_="value")
            if value_div:
                role_span = value_div.find("span", class_="role-name")
                if role_span:
                    profile.platform_role = role_span.get_text(strip=True)
                    logger.info(f"✅ 获取平台角色: {profile.platform_role}")
        
        # 获取Email (从 class="row collapse email")
        email_row = soup.find("div", class_="row collapse email")
        if email_row:
            value_div = email_row.find("div", class_="value")
            if value_div:
                email_span = value_div.find("span", class_="storage")
                if email_span:
                    profile.email = email_span.get_text(strip=True)
                    logger.info(f"✅ 获取Email: {profile.email}")
        
        # 方法2: 通过标题文本查找（用于系級等其他字段）
        rows = soup.find_all("div", class_="row collapse")
        logger.info(f"🔍 在全局找到 {len(rows)} 个 'row collapse' 行")

        for row in rows:
            # 获取标题
            title_div = row.find("div", class_="title")
            if not title_div:
                continue

            title_text = title_div.get_text(strip=True)

            # 获取值
            value_div = row.find("div", class_="value")
            if not value_div:
                continue

            # 只处理系級（其他字段已通过class直接获取）
            if title_text == "系級":
                span = value_div.find("span")
                if span:
                    profile.program = span.get_text(strip=True)
                    logger.info(f"✅ 获取系級: {profile.program}")

        logger.info(f"解析完成 -> 姓名: {profile.name_cn}, 英文姓名: {profile.name_en}, "
                   f"账号: {profile.account}, 系级: {profile.program}, "
                   f"平台角色: {profile.platform_role}, 邮箱: {profile.email}")
        return profile