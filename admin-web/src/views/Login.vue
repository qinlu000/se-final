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
  background: radial-gradient(circle at 20% 20%, #e0f2fe, transparent 25%),
    radial-gradient(circle at 80% 0%, #ede9fe, transparent 25%),
    #f8fafc;
}

.login-card {
  width: 360px;
  padding: 32px;
  background: #ffffff;
  box-shadow: 0 10px 30px rgba(15, 23, 42, 0.08);
  border-radius: 12px;
}

h2 {
  text-align: center;
  margin-bottom: 24px;
}
</style>
