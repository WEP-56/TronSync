<template>
  <ResizeBorder />
  <TitleBar />
  <div class="app-content">
    <router-view />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useThemeStore } from './store/theme'
import TitleBar from './components/TitleBar.vue'
import ResizeBorder from './components/ResizeBorder.vue'

const themeStore = useThemeStore()

onMounted(() => {
  console.log('App.vue onMounted')
  themeStore.applyTheme()
})
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  overflow: hidden; /* 防止出现双滚动条 */
}

#app {
  width: 100%;
  height: 100vh;
  background-color: var(--el-bg-color);
  color: var(--el-text-color-primary);
}

.app-content {
  height: 100vh;
  padding-top: 32px; /* TitleBar 高度 */
  overflow: hidden;
}

/* 滚动条样式优化 */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: transparent;
}

::-webkit-scrollbar-thumb {
  background: #dcdfe6;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #c0c4cc;
}
</style>
