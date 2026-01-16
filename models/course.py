from dataclasses import dataclass
from typing import List

@dataclass
class Course:
    """课程数据模型"""
    course_id: str = ""           # 课程ID
    name: str = ""                # 课程名称（display_name）
    course_code: str = ""         # 科目代码
    semester: str = ""            # 学期（如：2025第二學期）
    department: str = ""          # 系级（如：計算機科學碩士學位課程 (MCSBF)）
    grade: str = ""               # 年级（如：1年級）
    klass: str = ""               # 班级（如：A00）
    start_date: str = ""          # 开课日期
    end_date: str = ""            # 结束日期
    teaching_class: str = ""      # 授课班级（如：全學年課、學期課）
    compulsory: str = ""          # 必选修别（必修/選修）
    credit: str = ""              # 学分数
    instructors: List[str] = None # 授课教师列表
    cover_url: str = ""           # 课程封面URL
    course_url: str = ""          # 课程链接

    def __post_init__(self):
        if self.instructors is None:
            self.instructors = []

    def to_display_text(self):
        """生成用于 GUI 显示的格式化文本"""
        text_lines = [
            f"【课程名称】: {self.name}",
            f"【科目代码】: {self.course_code}",
            f"【学期】: {self.semester}",
            f"【系级】: {self.department}",
            f"【年级】: {self.grade}",
            f"【班级】: {self.klass}",
            f"【开课日期】: {self.start_date}",
            f"【结束日期】: {self.end_date}",
            f"【授课班级】: {self.teaching_class}",
            f"【必选修别】: {self.compulsory}",
            f"【学分数】: {self.credit}",
            f"【授课教师】: {', '.join(self.instructors) if self.instructors else '未获取'}",
        ]
        return "\n".join(text_lines)
