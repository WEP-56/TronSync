/**
 * 课程表时间段配置
 * 每个时间段为30分钟或15分钟
 */

export const TIME_SLOTS = [
  { id: 1, start: '08:00', end: '08:30' },
  { id: 2, start: '08:30', end: '09:00' },
  { id: 3, start: '09:00', end: '09:30' },
  { id: 4, start: '09:30', end: '09:45' },
  { id: 5, start: '09:45', end: '10:00' },
  { id: 6, start: '10:00', end: '10:15' },
  { id: 7, start: '10:15', end: '10:30' },
  { id: 8, start: '10:30', end: '11:00' },
  { id: 9, start: '11:00', end: '11:30' },
  { id: 10, start: '11:30', end: '12:00' },
  { id: 11, start: '12:15', end: '12:30' },
  { id: 12, start: '12:30', end: '12:45' },
  { id: 13, start: '12:45', end: '13:00' },
  { id: 14, start: '13:00', end: '13:15' },
  { id: 15, start: '13:15', end: '13:45' },
  { id: 16, start: '13:45', end: '14:00' },
  { id: 17, start: '14:00', end: '14:15' },
  { id: 18, start: '14:15', end: '14:30' },
  { id: 19, start: '14:30', end: '14:45' },
  { id: 20, start: '14:45', end: '15:15' },
  { id: 21, start: '15:15', end: '15:30' },
  { id: 22, start: '15:30', end: '15:45' },
  { id: 23, start: '16:00', end: '16:30' },
  { id: 24, start: '16:30', end: '17:00' },
  { id: 25, start: '17:00', end: '17:15' },
  { id: 26, start: '17:15', end: '17:30' },
  { id: 27, start: '17:30', end: '17:45' },
  { id: 28, start: '17:45', end: '18:00' },
  { id: 29, start: '18:00', end: '18:30' },
  { id: 30, start: '18:30', end: '19:00' },
  { id: 31, start: '19:00', end: '19:15' },
  { id: 32, start: '19:15', end: '20:00' },
  { id: 33, start: '20:00', end: '20:30' },
  { id: 34, start: '20:30', end: '21:15' },
  { id: 35, start: '21:15', end: '21:30' },
  { id: 36, start: '21:30', end: '22:00' },
  { id: 37, start: '22:00', end: '22:15' },
  { id: 38, start: '22:30', end: '22:45' },
  { id: 39, start: '22:45', end: '23:00' }
]

/**
 * 判断课程时间是否在时间段范围内
 * @param {string} courseStart 课程开始时间 HH:MM
 * @param {string} courseEnd 课程结束时间 HH:MM
 * @param {string} slotStart 时间段开始时间 HH:MM
 * @param {string} slotEnd 时间段结束时间 HH:MM
 * @returns {boolean}
 */
export function isTimeInSlot(courseStart, courseEnd, slotStart, slotEnd) {
  const toMinutes = (time) => {
    const [h, m] = time.split(':').map(Number)
    return h * 60 + m
  }
  
  const cStart = toMinutes(courseStart)
  const cEnd = toMinutes(courseEnd)
  const sStart = toMinutes(slotStart)
  const sEnd = toMinutes(slotEnd)
  
  // 课程时间与时间段有重叠
  return cStart < sEnd && cEnd > sStart
}

/**
 * 计算课程跨越的时间段数量
 * @param {string} courseStart 课程开始时间
 * @param {string} courseEnd 课程结束时间
 * @returns {number}
 */
export function calculateSpanSlots(courseStart, courseEnd) {
  let count = 0
  for (const slot of TIME_SLOTS) {
    if (isTimeInSlot(courseStart, courseEnd, slot.start, slot.end)) {
      count++
    }
  }
  return count
}

/**
 * 获取课程开始的时间段索引
 * @param {string} courseStart 课程开始时间
 * @returns {number} 时间段ID，如果找不到返回-1
 */
export function getStartSlotId(courseStart) {
  for (const slot of TIME_SLOTS) {
    if (isTimeInSlot(courseStart, courseStart, slot.start, slot.end)) {
      return slot.id
    }
  }
  return -1
}

export default TIME_SLOTS
