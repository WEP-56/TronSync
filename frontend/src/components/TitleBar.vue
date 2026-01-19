<template>
  <div class="title-bar" :class="{ 'dark': isDark }">
    <div class="title-drag-area pywebview-drag-region">
      <div class="app-icon">
        <!-- 这里的图标可以替换为实际的 logo 图片 -->
        <el-icon :size="18" color="#409eff"><Reading /></el-icon>
      </div>
      <div class="app-title">TronSync - 校园助手</div>
    </div>
    
    <div class="window-controls">
      <div class="control-btn minimize-btn" @click="minimize">
        <el-icon><Minus /></el-icon>
      </div>
      <div class="control-btn maximize-btn" @click="maximize">
        <el-icon><FullScreen /></el-icon>
      </div>
      <div class="control-btn close-btn" @click="close">
        <el-icon><Close /></el-icon>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { Minus, FullScreen, Close, Reading } from '@element-plus/icons-vue'

const isDark = computed(() => document.documentElement.classList.contains('dark'))

const minimize = () => {
  if (window.pywebview) {
    window.pywebview.api.minimize()
  }
}

const maximize = () => {
  if (window.pywebview) {
    window.pywebview.api.maximize()
  }
}

const close = () => {
  if (window.pywebview) {
    window.pywebview.api.close()
  }
}
</script>

<style scoped>
.title-bar {
  height: 32px;
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #ffffff;
  border-bottom: 1px solid #dcdfe6;
  position: fixed;
  top: 0;
  left: 0;
  z-index: 9999;
  user-select: none;
  transition: background-color 0.3s, border-color 0.3s;
}

.title-bar.dark {
  background-color: #1e1e1e;
  border-bottom: 1px solid #333;
  color: #fff;
}

.title-drag-area {
  flex: 1;
  height: 100%;
  display: flex;
  align-items: center;
  -webkit-app-region: drag; /* 启用 CSS 拖拽 */
  padding-left: 10px;
  cursor: default;
}

.app-icon {
  display: flex;
  align-items: center;
  margin-right: 8px;
  pointer-events: none; /* 防止图标干扰点击 */
}

.app-title {
  font-size: 12px;
  font-weight: 500;
  color: #606266;
}

/* 暗黑模式适配 */
.dark .app-title {
  color: #909399;
}

.window-controls {
  display: flex;
  height: 100%;
  -webkit-app-region: no-drag; /* 按钮区域不可拖拽 */
}

.control-btn {
  width: 46px;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  transition: background-color 0.2s;
  color: #606266;
}

.title-bar.dark .control-btn {
  color: #ccc;
}

.control-btn:hover {
  background-color: #f2f2f2;
}

.title-bar.dark .control-btn:hover {
  background-color: #333;
}

.close-btn:hover {
  background-color: #f56c6c;
  color: white;
}

.title-bar.dark .close-btn:hover {
  background-color: #d32f2f;
  color: white;
}
</style>
