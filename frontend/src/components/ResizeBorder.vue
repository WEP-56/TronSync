<template>
  <div class="resize-borders">
    <div class="resize-border top" @mousedown="initResize($event, 'top')"></div>
    <div class="resize-border bottom" @mousedown="initResize($event, 'bottom')"></div>
    <div class="resize-border left" @mousedown="initResize($event, 'left')"></div>
    <div class="resize-border right" @mousedown="initResize($event, 'right')"></div>
    
    <div class="resize-border top-left" @mousedown="initResize($event, 'top-left')"></div>
    <div class="resize-border top-right" @mousedown="initResize($event, 'top-right')"></div>
    <div class="resize-border bottom-left" @mousedown="initResize($event, 'bottom-left')"></div>
    <div class="resize-border bottom-right" @mousedown="initResize($event, 'bottom-right')"></div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const isResizing = ref(false)
const startX = ref(0)
const startY = ref(0)
const startW = ref(0)
const startH = ref(0)
const startWinX = ref(0)
const startWinY = ref(0)
const currentDir = ref('')

const initResize = async (e, direction) => {
  if (e.button !== 0 || !window.pywebview) return
  
  e.preventDefault()
  
  // 获取当前窗口几何信息
  try {
    const geo = await window.pywebview.api.get_window_geometry()
    if (!geo) return

    isResizing.value = true
    currentDir.value = direction
    startX.value = e.screenX
    startY.value = e.screenY
    
    startWinX.value = geo.x
    startWinY.value = geo.y
    startW.value = geo.width
    startH.value = geo.height
    
    // 添加全局事件监听
    document.addEventListener('mousemove', handleMouseMove)
    document.addEventListener('mouseup', stopResize)
  } catch (err) {
    console.error('Failed to get window geometry', err)
  }
}

const handleMouseMove = (e) => {
  if (!isResizing.value) return
  
  // 计算鼠标移动距离
  const dx = e.screenX - startX.value
  const dy = e.screenY - startY.value
  
  let newX = startWinX.value
  let newY = startWinY.value
  let newW = startW.value
  let newH = startH.value
  
  // 根据方向调整
  // 最小尺寸限制
  const MIN_W = 800
  const MIN_H = 600
  
  if (currentDir.value.includes('right')) {
    newW = Math.max(MIN_W, startW.value + dx)
  }
  if (currentDir.value.includes('bottom')) {
    newH = Math.max(MIN_H, startH.value + dy)
  }
  if (currentDir.value.includes('left')) {
    const maxDX = startW.value - MIN_W
    const actualDX = Math.min(dx, maxDX)
    newW = startW.value - actualDX
    newX = startWinX.value + actualDX
  }
  if (currentDir.value.includes('top')) {
    const maxDY = startH.value - MIN_H
    const actualDY = Math.min(dy, maxDY)
    newH = startH.value - actualDY
    newY = startWinY.value + actualDY
  }
  
  // 调用后端 API 更新窗口
  window.pywebview.api.set_window_geometry(newX, newY, newW, newH)
}

const stopResize = () => {
  isResizing.value = false
  document.removeEventListener('mousemove', handleMouseMove)
  document.removeEventListener('mouseup', stopResize)
}
</script>

<style scoped>
.resize-borders {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none; /* 让中间区域可穿透 */
  z-index: 10000; /* 高于 TitleBar (9999) 以确保边缘可点击 */
}

.resize-border {
  position: absolute;
  pointer-events: auto; /* 边框可点击 */
  /* background: rgba(255, 0, 0, 0.2); 调试用 */
}

/* 边框厚度 */
.top, .bottom {
  height: 4px;
  width: 100%;
  left: 0;
  cursor: ns-resize;
}
.top { top: 0; }
.bottom { bottom: 0; }

.left, .right {
  width: 4px;
  height: 100%;
  top: 0;
  cursor: ew-resize;
}
.left { left: 0; }
.right { right: 0; }

/* 角落大小 */
.top-left, .top-right, .bottom-left, .bottom-right {
  width: 8px;
  height: 8px;
  z-index: 9999;
}

.top-left {
  top: 0;
  left: 0;
  cursor: nwse-resize;
}

.top-right {
  top: 0;
  right: 0;
  cursor: nesw-resize;
}

.bottom-left {
  bottom: 0;
  left: 0;
  cursor: nesw-resize;
}

.bottom-right {
  bottom: 0;
  right: 0;
  cursor: nwse-resize;
}
</style>