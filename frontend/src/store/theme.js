import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useThemeStore = defineStore('theme', () => {
  // 状态
  const themeMode = ref(localStorage.getItem('theme_mode') || 'light') // light, dark, auto
  const themeColor = ref(localStorage.getItem('theme_color') || '#409eff')
  
  // 预设主题
  const presetThemes = [
    { name: '默认蓝', color: '#409eff' },
    { name: '清新绿', color: '#67c23a' },
    { name: '活力橙', color: '#e6a23c' },
    { name: '热情红', color: '#f56c6c' },
    { name: '优雅紫', color: '#626aef' },
    { name: '沉稳灰', color: '#909399' },
    { name: '暗夜黑', color: '#000000' } // 特殊处理
  ]

  // Action: 应用主题
  const applyTheme = () => {
    const html = document.documentElement
    
    // 1. 应用模式 (Light/Dark)
    if (themeMode.value === 'dark') {
      html.classList.add('dark')
    } else if (themeMode.value === 'light') {
      html.classList.remove('dark')
    } else {
      // Auto: 跟随系统
      if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
        html.classList.add('dark')
      } else {
        html.classList.remove('dark')
      }
    }
    
    // 2. 应用主题色
    // Element Plus 使用 CSS 变量
    html.style.setProperty('--el-color-primary', themeColor.value)
    
    // 生成不同深浅的变体 (简单算法，Element Plus 官方有一套复杂的生成逻辑，这里简化)
    // 实际生产中最好引入 color 库来生成 mix 颜色
    // 这里我们简单设置几个关键变量，或者依赖 Element Plus 的默认混色机制(如果有)
    // 但 Element Plus 需要手动设置 --el-color-primary-light-x
    updateThemeColorVar(themeColor.value)

    // 持久化
    localStorage.setItem('theme_mode', themeMode.value)
    localStorage.setItem('theme_color', themeColor.value)
  }
  
  // 辅助：生成并设置颜色变体
  const updateThemeColorVar = (color) => {
    const el = document.documentElement
    // 这里使用一个简单的混色函数来模拟 Element Plus 的 lighten/darken
    // 为了简化，我们暂时只设置主色，让 Element Plus 自动降级或者稍后引入 tinycolor2
    // 如果不设置 light-x，hover 效果可能会有问题。
    // 让我们尝试手动计算几个简单的变体
    
    // 简单的十六进制转 RGB
    const hexToRgb = (hex) => {
      let r = 0, g = 0, b = 0
      if (hex.length === 4) {
        r = parseInt('0x' + hex[1] + hex[1])
        g = parseInt('0x' + hex[2] + hex[2])
        b = parseInt('0x' + hex[3] + hex[3])
      } else if (hex.length === 7) {
        r = parseInt('0x' + hex[1] + hex[2])
        g = parseInt('0x' + hex[3] + hex[4])
        b = parseInt('0x' + hex[5] + hex[6])
      }
      return [r, g, b]
    }
    
    const rgbToHex = (r, g, b) => {
      const toHex = (c) => {
        const hex = Math.round(c).toString(16)
        return hex.length === 1 ? '0' + hex : hex
      }
      return `#${toHex(r)}${toHex(g)}${toHex(b)}`
    }
    
    const mix = (c1, c2, ratio) => {
      const r = c1[0] * (1 - ratio) + c2[0] * ratio
      const g = c1[1] * (1 - ratio) + c2[1] * ratio
      const b = c1[2] * (1 - ratio) + c2[2] * ratio
      return [r, g, b]
    }
    
    const baseRgb = hexToRgb(color)
    const whiteRgb = [255, 255, 255]
    const blackRgb = [0, 0, 0]
    
    // 生成 light-3, light-5, light-7, light-8, light-9, dark-2
    const levels = {
      'light-3': 0.3,
      'light-5': 0.5,
      'light-7': 0.7,
      'light-8': 0.8,
      'light-9': 0.9,
      'dark-2': 0.2
    }
    
    Object.keys(levels).forEach(key => {
      const value = levels[key]
      const mixed = key.includes('dark') 
        ? mix(blackRgb, baseRgb, value) 
        : mix(whiteRgb, baseRgb, value)
      const hex = rgbToHex(mixed[0], mixed[1], mixed[2])
      el.style.setProperty(`--el-color-primary-${key}`, hex)
    })
  }

  // 切换模式
  const setMode = (mode) => {
    themeMode.value = mode
    applyTheme()
  }

  // 设置颜色
  const setColor = (color) => {
    themeColor.value = color
    applyTheme()
  }

  return {
    themeMode,
    themeColor,
    presetThemes,
    applyTheme,
    setMode,
    setColor
  }
})
