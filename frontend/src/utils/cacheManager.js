// 数据缓存管理
// 用于控制数据请求频率，避免频繁请求导致被封

const CACHE_KEYS = {
  COURSES: 'cached_courses',
  ANNOUNCEMENTS: 'cached_announcements',
  SCHEDULE: 'cached_schedule',
  USER_PROFILE: 'cached_user_profile'
}

const CACHE_TIMESTAMP_KEYS = {
  COURSES: 'cache_timestamp_courses',
  ANNOUNCEMENTS: 'cache_timestamp_announcements',
  SCHEDULE: 'cache_timestamp_schedule',
  USER_PROFILE: 'cache_timestamp_user_profile'
}

// 缓存过期时间（毫秒）
const CACHE_EXPIRE_TIME = 5 * 60 * 1000 // 5分钟

class CacheManager {
  // 保存数据到缓存
  static setCache(key, data) {
    try {
      localStorage.setItem(CACHE_KEYS[key], JSON.stringify(data))
      localStorage.setItem(CACHE_TIMESTAMP_KEYS[key], Date.now().toString())
      console.log(`✅ 缓存已保存: ${key}`)
    } catch (e) {
      console.error(`❌ 缓存保存失败: ${key}`, e)
    }
  }

  // 从缓存获取数据
  static getCache(key, forceRefresh = false) {
    try {
      // 如果强制刷新，直接返回null
      if (forceRefresh) {
        console.log(`🔄 强制刷新: ${key}`)
        return null
      }

      const timestamp = localStorage.getItem(CACHE_TIMESTAMP_KEYS[key])
      const now = Date.now()

      // 检查是否过期
      if (timestamp && (now - parseInt(timestamp)) < CACHE_EXPIRE_TIME) {
        const data = localStorage.getItem(CACHE_KEYS[key])
        if (data) {
          console.log(`📦 使用缓存: ${key}`)
          return JSON.parse(data)
        }
      } else {
        console.log(`⏰ 缓存已过期: ${key}`)
      }
    } catch (e) {
      console.error(`❌ 缓存读取失败: ${key}`, e)
    }
    return null
  }

  // 清除指定缓存
  static clearCache(key) {
    localStorage.removeItem(CACHE_KEYS[key])
    localStorage.removeItem(CACHE_TIMESTAMP_KEYS[key])
    console.log(`🗑️ 缓存已清除: ${key}`)
  }

  // 清除所有缓存
  static clearAllCache() {
    Object.values(CACHE_KEYS).forEach(key => {
      localStorage.removeItem(key)
    })
    Object.values(CACHE_TIMESTAMP_KEYS).forEach(key => {
      localStorage.removeItem(key)
    })
    console.log('🗑️ 所有缓存已清除')
  }

  // 检查缓存是否有效
  static isCacheValid(key) {
    const timestamp = localStorage.getItem(CACHE_TIMESTAMP_KEYS[key])
    if (!timestamp) return false
    
    const now = Date.now()
    return (now - parseInt(timestamp)) < CACHE_EXPIRE_TIME
  }
}

export default CacheManager
export { CACHE_KEYS }
