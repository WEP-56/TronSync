/**
 * 学年学期管理工具
 * 
 * 规则：
 * - 学年从8月17日开始（例如2025学年从2025-08-17开始）
 * - 第一学期：8月17日（周日）- 次年1月4日（周日）（21周）
 * - 第二学期：次年1月4日（周日）- 次年8月16日（周六）（31周）
 * - 注意：1月4日既是第一学期的最后一天，也是第二学期的第一天
 * - 一周从周日开始，到周六结束
 */

export class SemesterManager {
  /**
   * 获取指定日期所属的学年
   * @param {Date} date 
   * @returns {number} 学年年份
   */
  static getAcademicYear(date = new Date()) {
    const year = date.getFullYear()
    const month = date.getMonth() + 1
    const day = date.getDate()
    
    // 8月17日之前属于上一学年
    if (month < 8 || (month === 8 && day < 17)) {
      return year - 1
    }
    return year
  }
  
  /**
   * 获取指定日期所属的学期
   * @param {Date} date 
   * @returns {number} 1 或 2
   */
  static getSemester(date = new Date()) {
    const year = date.getFullYear()
    const month = date.getMonth() + 1
    const day = date.getDate()
    
    // 1月4日到8月16日是第二学期
    if (month < 8 || (month === 8 && day <= 16)) {
      return 2
    }
    // 8月17日到次年1月4日是第一学期
    return 1
  }
  
  /**
   * 获取学期的开始日期
   * @param {number} academicYear 学年
   * @param {number} semester 学期 (1 或 2)
   * @returns {Date}
   */
  static getSemesterStartDate(academicYear, semester) {
    if (semester === 1) {
      // 第一学期从8月17日开始
      return new Date(academicYear, 7, 17) // 月份从0开始，7=8月
    } else {
      // 第二学期从当年1月4日开始（注意：是academicYear+1年）
      return new Date(academicYear + 1, 0, 4) // 0=1月
    }
  }
  
  /**
   * 获取学期的结束日期
   * @param {number} academicYear 学年
   * @param {number} semester 学期 (1 或 2)
   * @returns {Date}
   */
  static getSemesterEndDate(academicYear, semester) {
    if (semester === 1) {
      // 第一学期到次年1月4日结束（包含1月4日）
      return new Date(academicYear + 1, 0, 4)
    } else {
      // 第二学期到当年8月16日结束
      return new Date(academicYear + 1, 7, 16)
    }
  }
  
  /**
   * 获取学期的总周数
   * @param {number} semester 学期 (1 或 2)
   * @returns {number}
   */
  static getSemesterWeeks(semester) {
    return semester === 1 ? 21 : 31
  }
  
  /**
   * 获取指定周的日期范围（周日到周六）
   * @param {number} academicYear 学年
   * @param {number} semester 学期
   * @param {number} week 周数
   * @returns {Object} { start: Date, end: Date, dates: Date[] }
   */
  static getWeekDates(academicYear, semester, week) {
    const semesterStart = this.getSemesterStartDate(academicYear, semester)
    
    // 计算该周的开始日期（周日）
    const weekStart = new Date(semesterStart)
    weekStart.setDate(semesterStart.getDate() + (week - 1) * 7)
    
    // 生成一周的日期（周日到周六）
    const dates = []
    for (let i = 0; i < 7; i++) {
      const date = new Date(weekStart)
      date.setDate(weekStart.getDate() + i)
      dates.push(date)
    }
    
    const weekEnd = new Date(weekStart)
    weekEnd.setDate(weekStart.getDate() + 6)
    
    return {
      start: weekStart,
      end: weekEnd,
      dates: dates
    }
  }
  
  /**
   * 获取当前周数
   * @returns {Object} { academicYear, semester, week }
   */
  static getCurrentWeek() {
    const now = new Date()
    const academicYear = this.getAcademicYear(now)
    const semester = this.getSemester(now)
    const semesterStart = this.getSemesterStartDate(academicYear, semester)
    
    // 计算从学期开始到现在的天数
    const diffTime = now - semesterStart
    const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24))
    
    // 计算周数（从1开始）
    const week = Math.floor(diffDays / 7) + 1
    
    // 确保周数在有效范围内
    const maxWeeks = this.getSemesterWeeks(semester)
    const validWeek = Math.max(1, Math.min(week, maxWeeks))
    
    return {
      academicYear,
      semester,
      week: validWeek
    }
  }
  
  /**
   * 格式化日期为 MM/DD 格式
   * @param {Date} date 
   * @returns {string}
   */
  static formatDate(date) {
    const month = date.getMonth() + 1
    const day = date.getDate()
    return `${month}/${day}`
  }
  
  /**
   * 格式化星期
   * @param {number} dayIndex 0=周日, 1=周一, ..., 6=周六
   * @returns {string}
   */
  static formatWeekDay(dayIndex) {
    const days = ['周日', '周一', '周二', '周三', '周四', '周五', '周六']
    return days[dayIndex]
  }
}

export default SemesterManager
