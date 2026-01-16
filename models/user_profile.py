from dataclasses import dataclass

@dataclass
class UserProfile:
    """用户个人资料数据模型"""
    name_cn: str = ""          # 姓名（如：潘世鼎 PAN SHIDING）
    name_en: str = ""          # 英文姓名（如：PAN SHIDING）
    avatar_url: str = ""       # 头像 URL
    platform_role: str = ""    # 平台角色（如：學生）
    account: str = ""          # 账号（如：D25091111032）
    program: str = ""          # 系级（如：計算機科學碩士學位課程 (MCSBF)1年級B）
    email: str = ""            # 邮箱（如果在其他板块）

    def to_display_text(self):
        """
        生成用于 GUI 显示的格式化文本。
        包含头像链接，方便复制查看。
        """
        text_lines = [
            f"【姓名】: {self.name_cn}",
            f"【英文姓名】: {self.name_en}",
            f"【账号】: {self.account}",
            f"【系级】: {self.program}",
            f"【平台角色】: {self.platform_role}",
            f"【邮箱】: {self.email if self.email else '未获取'}",
            f"\n【头像链接】:\n{self.avatar_url if self.avatar_url else '未获取'}"
        ]
        return "\n".join(text_lines)