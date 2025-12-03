<template>
  <view class="page">
    <view class="card">
      <view class="title">{{ isRegister ? '注册账号' : '用户登录' }}</view>
      
      <view class="form-item">
        <text class="label">用户名</text>
        <input v-model="username" placeholder="输入用户名" />
      </view>
      
      <view class="form-item" v-if="isRegister">
        <text class="label">昵称</text>
        <input v-model="nickname" placeholder="输入昵称 (可选)" />
      </view>

      <view class="form-item">
        <text class="label">密码</text>
        <input v-model="password" password placeholder="输入密码" />
      </view>
      
      <button class="submit" :disabled="loading" @click="submit">
        {{ isRegister ? '注册并登录' : '登录' }}
      </button>

      <view class="switch-mode" @click="toggleMode">
        {{ isRegister ? '已有账号？去登录' : '没有账号？去注册' }}
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref } from 'vue'
import { request } from '../../utils/request'

const isRegister = ref(false)
const username = ref('')
const password = ref('')
const nickname = ref('')
const loading = ref(false)

const toggleMode = () => {
  isRegister.value = !isRegister.value
  username.value = ''
  password.value = ''
  nickname.value = ''
}

const submit = async () => {
  if (!username.value || !password.value) {
    uni.showToast({ title: '请输入账号密码', icon: 'none' })
    return
  }
  
  loading.value = true
  try {
    if (isRegister.value) {
      // Register
      await request({
        url: '/auth/register',
        method: 'POST',
        data: {
          username: username.value,
          password: password.value,
          nickname: nickname.value || undefined
        }
      })
      uni.showToast({ title: '注册成功', icon: 'success' })
      // Auto login after register
      await login()
    } else {
      // Login
      await login()
    }
  } catch (err) {
    console.error(err)
    const msg = err?.data?.detail || (isRegister.value ? '注册失败' : '登录失败')
    uni.showToast({ title: msg, icon: 'none' })
  } finally {
    loading.value = false
  }
}

const login = async () => {
  const body = `username=${encodeURIComponent(username.value)}&password=${encodeURIComponent(password.value)}`
  const res = await request({
    url: '/auth/token',
    method: 'POST',
    data: body,
    header: { 'Content-Type': 'application/x-www-form-urlencoded' },
  })

  uni.setStorageSync('token', res.access_token)
  uni.showToast({ title: '登录成功', icon: 'success' })
  setTimeout(() => {
    uni.switchTab({ url: '/pages/index/index' })
  }, 400)
}
</script>

<style scoped>
.page {
  min-height: 100vh;
  background: #ededed;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24rpx;
  box-sizing: border-box;
}

.card {
  width: 90%;
  max-width: 640rpx;
  background: #ffffff;
  border-radius: 18rpx;
  padding: 40rpx 32rpx;
  box-shadow: 0 12rpx 30rpx rgba(0, 0, 0, 0.08);
}

.title {
  font-size: 36rpx;
  font-weight: 700;
  text-align: center;
  margin-bottom: 32rpx;
}

.form-item {
  margin-bottom: 24rpx;
}

.label {
  display: block;
  margin-bottom: 8rpx;
  color: #4b5563;
}

input {
  width: 100%;
  height: 88rpx;
  border-radius: 12rpx;
  padding: 0 16rpx;
  background: #f3f4f6;
  box-sizing: border-box;
}

.submit {
  width: 100%;
  height: 88rpx;
  border-radius: 12rpx;
  background: #07c160;
  color: #ffffff;
  font-size: 30rpx;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
}

.switch-mode {
  text-align: center;
  margin-top: 24rpx;
  color: #07c160;
  font-size: 28rpx;
}
</style>
