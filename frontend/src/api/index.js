import axios from 'axios'
import { ElMessage } from 'element-plus'

const api = axios.create({
  baseURL: import.meta.env.DEV ? '/api' : 'http://127.0.0.1:5000/api',
  timeout: 30000,
  withCredentials: true
})

// 请求拦截器
api.interceptors.request.use(
  config => {
    return config
  },
  error => {
    console.error('请求错误:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  response => {
    return response.data
  },
  error => {
    console.error('响应错误:', error)
    
    if (error.response) {
      const status = error.response.status
      if (status === 401) {
        ElMessage.error('未登录或登录已过期')
        localStorage.removeItem('isLoggedIn')
        window.location.href = '/login'
      } else if (status === 500) {
        ElMessage.error('服务器错误，请稍后重试')
      }
    } else {
      ElMessage.error('网络错误，请检查连接')
    }
    
    return Promise.reject(error)
  }
)

// API方法
export default {
  // 登录
  login(username, password) {
    return api.post('/login', { username, password })
  },
  
  // 登出
  logout() {
    return api.post('/logout')
  },
  
  // 检查登录状态
  checkLogin() {
    return api.get('/check-login')
  },
  
  // 获取用户信息
  getUserProfile() {
    return api.get('/user/profile')
  },
  
  // 获取课程列表
  getCourses() {
    return api.get('/courses')
  },
  
  // 获取公告列表
  getAnnouncements() {
    return api.get('/announcements')
  },
  
  // 获取课程表
  getSchedule() {
    return api.get('/schedule')
  },
  
  // 获取文件列表
  getFiles(params = {}) {
    return api.get('/files', { params })
  },
  
  // 获取保存的登录凭证
  getCredentials() {
    return api.get('/config/credentials')
  },
  
  // 保存登录凭证
  saveCredentials(data) {
    return api.post('/config/credentials', data)
  },
  
  // 获取设置
  getSettings() {
    return api.get('/config/settings')
  },
  
  // 保存设置
  saveSettings(data) {
    return api.post('/config/settings', data)
  },
  
  // 选择文件夹
  selectFolder() {
    return api.post('/system/select-folder')
  },
  
  // 下载文件
  downloadFile(fileId, fileName) {
    return api.post('/files/download', { file_id: fileId, file_name: fileName })
  },
  
  // 检查更新
  checkUpdate() {
    return api.get('/system/check-update')
  },
  
  // 执行更新
  performUpdate(downloadUrl) {
    return api.post('/system/perform-update', { download_url: downloadUrl })
  }
}
