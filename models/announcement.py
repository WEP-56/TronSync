from dataclasses import dataclass

@dataclass
class Announcement:
    """公告数据模型"""
    title: str = ""          # 标题 (如: 课程日程安排)
    course_name: str = ""    # 课程名称 (如: 神經網絡)
    created_at: str = ""      # 发布时间 (如: 2026.01.06 13:53)
    target: str = ""          # 目标人群 (如: 所有人)
    content: str = ""         # 公告正文 (HTML格式)