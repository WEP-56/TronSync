from dataclasses import dataclass
from typing import List

@dataclass
class CourseSchedule:
    """课程表单节课数据模型"""
    course_name: str = ""          # 课程名称
    teacher: str = ""              # 授课教师
    classroom: str = ""            # 教室
    week_day: int = 0              # 星期几 (1-7, 1=星期一)
    start_time: str = ""           # 开始时间
    end_time: str = ""             # 结束时间
    start_section: int = 0         # 开始节次
    end_section: int = 0           # 结束节次
    weeks: str = ""                # 周次（如：1-16周）
    course_type: str = ""          # 课程类型（必修/选修）
    credits: str = ""              # 学分

    def __post_init__(self):
        """数据验证"""
        if self.week_day < 1 or self.week_day > 7:
            self.week_day = 0

    def get_week_day_name(self):
        """获取星期名称"""
        week_names = {
            1: "星期一",
            2: "星期二", 
            3: "星期三",
            4: "星期四",
            5: "星期五",
            6: "星期六",
            7: "星期日"
        }
        return week_names.get(self.week_day, "未知")

    def get_time_range(self):
        """获取时间范围"""
        if self.start_time and self.end_time:
            return f"{self.start_time}-{self.end_time}"
        elif self.start_section and self.end_section:
            return f"第{self.start_section}-{self.end_section}节"
        return ""

    def to_display_text(self):
        """生成用于 GUI 显示的格式化文本"""
        text_lines = [
            f"【课程名称】: {self.course_name}",
            f"【授课教师】: {self.teacher}",
            f"【上课时间】: {self.get_week_day_name()} {self.get_time_range()}",
            f"【上课地点】: {self.classroom}",
            f"【周次】: {self.weeks}",
        ]
        if self.course_type:
            text_lines.append(f"【课程类型】: {self.course_type}")
        if self.credits:
            text_lines.append(f"【学分】: {self.credits}")
        return "\n".join(text_lines)


@dataclass
class WeekSchedule:
    """一周的课程表"""
    week_number: int = 0           # 第几周
    schedules: List[CourseSchedule] = None  # 课程列表

    def __post_init__(self):
        if self.schedules is None:
            self.schedules = []

    def get_day_schedules(self, week_day: int):
        """获取某一天的课程"""
        return [s for s in self.schedules if s.week_day == week_day]

    def to_display_text(self):
        """生成用于 GUI 显示的格式化文本"""
        if not self.schedules:
            return "本周暂无课程安排"
        
        text = f"第 {self.week_number} 周课程表\n"
        text += "=" * 60 + "\n\n"
        
        # 按星期分组显示
        for day in range(1, 8):
            day_schedules = self.get_day_schedules(day)
            if day_schedules:
                text += f"【{day_schedules[0].get_week_day_name()}】\n"
                for idx, schedule in enumerate(day_schedules, 1):
                    text += f"  {idx}. {schedule.course_name}\n"
                    text += f"     时间: {schedule.get_time_range()}\n"
                    text += f"     地点: {schedule.classroom}\n"
                    text += f"     教师: {schedule.teacher}\n"
                text += "\n"
        
        return text
