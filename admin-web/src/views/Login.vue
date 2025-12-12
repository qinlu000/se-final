<template>
  <div class="login-page">
    <div class="login-card">
      <h2>管理员登录</h2>
      <el-form ref="formRef" :model="form" :rules="rules" label-position="top">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="form.username" placeholder="输入用户名" />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="form.password" type="password" placeholder="输入密码" show-password />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="loading" style="width: 100%" @click="onSubmit">登录</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElForm, ElMessage } from 'element-plus'

import api from '../api'

interface LoginForm {
  username: string
  password: string
}

const router = useRouter()
const route = useRoute()
const loading = ref(false)
const formRef = ref<InstanceType<typeof ElForm>>()
const form = reactive<LoginForm>({
  username: '',
  password: '',
})

const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
}

const onSubmit = () => {
  if (!formRef.value) return
  formRef.value.validate(async (valid) => {
    if (!valid) return
    loading.value = true
    try {
      const data = new URLSearchParams()
      data.append('username', form.username)
      data.append('password', form.password)

      const res = await api.post('/auth/token', data, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      })

      localStorage.setItem('token', res.data.access_token)
      ElMessage.success('登录成功')
      const redirectPath = (route.query.redirect as string) || '/users'
      router.push(redirectPath)
    } catch (error: any) {
      const detail = error?.response?.data?.detail || '登录失败'
      ElMessage.error(detail)
    } finally {
      loading.value = false
    }
  })
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 32px;
  background-color: #f3f3f3;
  background-image: radial-gradient(#dcdcdc 1px, transparent 1px);
  background-size: 18px 18px;
  font-family: 'DM Mono', 'SFMono-Regular', 'Menlo', monospace;
}

.login-card {
  width: 400px;
  padding: 36px;
  background: #ffffff;
  border: 2px solid #000000;
  box-shadow: 8px 8px 0px #000000;
  border-radius: 12px;
}

h2 {
  text-align: center;
  margin-bottom: 28px;
  font-weight: 900;
  letter-spacing: 0.5px;
}

:deep(.el-form-item) {
  margin-bottom: 20px;
}

:deep(.el-form-item__label) {
  font-weight: 800;
  color: #000000;
}

:deep(.el-input__wrapper) {
  border-radius: 12px;
  border: 2px solid #000000;
  box-shadow: 4px 4px 0px #000000 !important;
  background: #ffffff;
  transition: background 0.12s ease, box-shadow 0.12s ease, transform 0.12s ease;
}

:deep(.el-input__wrapper:hover) {
  box-shadow: 2px 2px 0px #000000 !important;
}

:deep(.el-input__wrapper.is-focus),
:deep(.el-input__wrapper.is-focus-within) {
  background: #ffe600;
  box-shadow: none !important;
}

:deep(.el-button--primary) {
  width: 100%;
  background: #ffe600;
  color: #000000;
  border: 2px solid #000000;
  box-shadow: 8px 8px 0px #000000;
  border-radius: 12px;
  font-weight: 900;
  transition: transform 0.1s ease, box-shadow 0.1s ease, background 0.1s ease;
}

:deep(.el-button--primary:hover) {
  background: #fff177;
}

:deep(.el-button--primary:active) {
  box-shadow: none;
  transform: translate(6px, 6px);
}
</style>
