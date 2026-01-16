import requests
import logging
import re
from requests.exceptions import RequestException, Timeout
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class SessionManager:
    def __init__(self):
        self.session = requests.Session()
        self.is_logged_in = False

        # 伪装浏览器
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })

    def login(self, username, password):
        """
        处理 CAS 认证流程 - 极简版：只发送必要的隐藏字段
        """
        tron_login_url = "https://tronclass.cityu.edu.mo/login"

        try:
            # 第一步：获取 CAS 登录页
            logger.info("正在获取 CAS 登录入口...")
            resp = self.session.get(tron_login_url, timeout=10)
            cas_login_url = resp.url
            logger.info(f"跳转至 CAS 登录页: {cas_login_url}")

            if "login.cityu.edu.mo" not in cas_login_url:
                logger.error("未检测到 CAS 跳转。")
                return False

            # 第二步：解析并抓取隐藏字段 (仅限 type="hidden")
            soup = BeautifulSoup(resp.text, "html.parser")

            # 初始化 POST 数据字典
            payload = {}

            hidden_inputs = soup.find_all("input", {"type": "hidden"})
            logger.info(f"找到 {len(hidden_inputs)} 个隐藏字段。")

            for inp in hidden_inputs:
                name = inp.get("name")
                value = inp.get("value", "")
                if name:
                    payload[name] = value
                    if name in ["lt", "execution", "_eventId"]:
                        logger.info(f"  - {name}: {value[:20]}...")

            # 【修改点】只加入账号密码，不加任何多余参数
            payload['username'] = username
            payload['password'] = password

            logger.info(f"准备提交 Payload (共 {len(payload)} 个字段): {list(payload.keys())}")

            # 第三步：构造 Headers
            cas_headers = {
                'Referer': cas_login_url,
                'Origin': 'https://login.cityu.edu.mo',
                'Content-Type': 'application/x-www-form-urlencoded'
            }

            # 第四步：发送 POST 请求
            # 目标 URL 包含了 service 参数，我们不再 Body 里重复加
            logger.info("正在向 CAS 服务器发送登录请求...")
            login_resp = self.session.post(
                cas_login_url,
                data=payload,
                headers=cas_headers,
                timeout=10,
                allow_redirects=True
            )

            logger.info(f"CAS 响应状态码: {login_resp.status_code}")
            logger.info(f"CAS 处理后最终 URL: {login_resp.url}")

            # 第五步：判断结果
            # 检查是否还在登录页 (通过 URL 判断)
            if "login.cityu.edu.mo" in login_resp.url and "login" in login_resp.url:
                logger.error("登录失败：停留在 CAS 登录页。")
                # 尝试解析错误信息
                err_soup = BeautifulSoup(login_resp.text, "html.parser")
                err_div = err_soup.find("div", class_="errors") or err_soup.find("span", id="msg")
                if err_div:
                    logger.error(f"错误信息: {err_div.get_text(strip=True)}")
                else:
                    # 如果是 500，这里应该能捕捉到
                    title_tag = err_soup.find("title")
                    if title_tag:
                        logger.error(f"页面标题: {title_tag.string}")
                return False

            # 第六步：最终验证
            verify_url = "https://tronclass.cityu.edu.mo/user/settings#/"
            logger.info("正在验证 TronClass 会话...")
            verify_resp = self.session.get(verify_url, timeout=10)

            if verify_resp.status_code == 200 and "login" not in verify_resp.url:
                logger.info("✅ 登录成功！且会话有效。")
                self.is_logged_in = True
                return True
            else:
                logger.error(f"❌ 验证失败。最终 URL: {verify_resp.url}")
                return False

        except Timeout:
            logger.error("请求超时")
            return False
        except Exception as e:
            logger.error(f"登录过程发生异常: {e}", exc_info=True)
            return False

    def get_session(self):
        return self.session
    
    def clear_session(self):
        """清除session和登录状态"""
        self.session.cookies.clear()
        self.is_logged_in = False
        logger.info("已清除session")