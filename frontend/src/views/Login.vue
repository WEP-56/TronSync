<template>
  <div class="login-container">
    <div class="login-box">
      <div class="login-header">
        <h1>TronSync</h1>
        <p>校园助手</p>
      </div>
      
      <el-form :model="loginForm" :rules="rules" ref="loginFormRef" class="login-form">
        <el-form-item prop="username">
          <el-input
            v-model="loginForm.username"
            placeholder="学号/用户名"
            prefix-icon="User"
            size="large"
          />
        </el-form-item>
        
        <el-form-item prop="password">
          <el-input
            v-model="loginForm.password"
            type="password"
            placeholder="密码"
            prefix-icon="Lock"
            size="large"
            @keyup.enter="handleLogin"
          />
        </el-form-item>
        
        <el-form-item>
          <div class="remember-options">
            <el-checkbox v-model="rememberPassword" label="保存密码" />
            <el-checkbox v-model="autoLogin" label="自动登录" />
          </div>
        </el-form-item>
        
        <el-form-item>
          <el-button
            type="primary"
            size="large"
            :loading="loading"
            @click="handleLogin"
            class="login-button"
          >
            {{ loading ? '登录中...' : '登录' }}
          </el-button>
        </el-form-item>
      </el-form>
      
      <div class="login-footer">
        <p>首次使用请输入TronClass账号密码</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import api from '../api'

const router = useRouter()
const loginFormRef = ref(null)
const loading = ref(false)
const rememberPassword = ref(true)  // 默认勾选
const autoLogin = ref(false)

const loginForm = reactive({
  username: '',
  password: ''
})

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' }
  ]
}

// 加载保存的登录信息
const loadSavedCredentials = async () => {
  try {
    console.log('📦 从服务器加载保存的凭证...')
    const response = await api.getCredentials()
    if (response.success && response.data) {
      const { username, password, remember_password, auto_login } = response.data
      console.log('👤 用户名:', username, '| 记住密码:', remember_password, '| 自动登录:', auto_login)
      
      if (remember_password && username) {
        loginForm.username = username
        loginForm.password = password || ''
        rememberPassword.value = remember_password
        autoLogin.value = auto_login || false
        console.log('✅ 已填充保存的凭证')
      }
    }
  } catch (e) {
    console.error('❌ 加载保存的凭证失败:', e)
  }
}

// 自动登录
const autoLoginIfEnabled = async () => {
  try {
    const response = await api.getCredentials()
    if (response.success && response.data) {
      const { username, password, auto_login } = response.data
      if (auto_login && username && password) {
        // 检查是否已经登录
        const isAlreadyLoggedIn = localStorage.getItem('isLoggedIn') === 'true'
        if (isAlreadyLoggedIn) {
          console.log('✅ 已登录，直接跳转到主页')
          router.push('/home')
          return
        }
        
        // 未登录，执行自动登录
        console.log('🔄 开始自动登录...')
        loginForm.username = username
        loginForm.password = password
        autoLogin.value = true
        rememberPassword.value = true
        
        // 延迟500ms后自动登录
        setTimeout(() => {
          handleLogin()
        }, 500)
      }
    }
  } catch (e) {
    console.error('自动登录失败:', e)
  }
}

const handleLogin = async () => {
  if (!loginFormRef.value) return
  
  await loginFormRef.value.validate(async (valid) => {
    if (!valid) return
    
    loading.value = true
    
    try {
      const response = await api.login(loginForm.username, loginForm.password)
      
      if (response.success) {
        ElMessage.success('登录成功！')
        
        // 保存登录状态到 localStorage（临时）
        localStorage.setItem('isLoggedIn', 'true')
        localStorage.setItem('username', loginForm.username)
        
        // 保存凭证到服务器（持久化）
        try {
          await api.saveCredentials({
            username: loginForm.username,
            password: loginForm.password,
            remember_password: rememberPassword.value,
            auto_login: autoLogin.value
          })
          console.log('✅ 凭证已保存到服务器')
        } catch (e) {
          console.error('❌ 保存凭证失败:', e)
        }
        
        setTimeout(() => {
          router.push('/home')
        }, 500)
      } else {
        ElMessage.error(response.message || '登录失败')
      }
    } catch (error) {
      console.error('登录错误:', error)
      ElMessage.error('登录失败，请检查网络连接')
    } finally {
      loading.value = false
    }
  })
}

onMounted(() => {
  // 加载保存的登录信息
  loadSavedCredentials()
  
  // 执行自动登录（如果启用）
  autoLoginIfEnabled()
})
</script>

<style scoped>
.login-container {
  width: 100%;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.login-box {
  width: 400px;
  padding: 40px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.login-header {
  text-align: center;
  margin-bottom: 40px;
}

.login-header h1 {
  font-size: 32px;
  font-weight: bold;
  color: #333;
  margin-bottom: 8px;
}

.login-header p {
  font-size: 14px;
  color: #999;
}

.login-form {
  margin-top: 20px;
}

.login-button {
  width: 100%;
  margin-top: 10px;
}

.login-footer {
  text-align: center;
  margin-top: 20px;
}

.login-footer p {
  font-size: 12px;
  color: #999;
}

.remember-options {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
