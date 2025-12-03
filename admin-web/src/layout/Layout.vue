<template>
  <el-container class="layout">
    <el-aside width="200px" class="aside">
      <div class="logo">Moments Admin</div>
      <el-menu
        router
        :default-active="activeMenu"
        background-color="#1f2937"
        text-color="#e5e7eb"
        active-text-color="#409eff"
      >
        <el-menu-item index="/users">
          <el-icon><UserFilled /></el-icon>
          <span>用户管理</span>
        </el-menu-item>
        <el-menu-item index="/posts">
          <el-icon><Document /></el-icon>
          <span>内容管理</span>
        </el-menu-item>
        <el-menu-item index="/stats">
          <el-icon><DataAnalysis /></el-icon>
          <span>数据统计</span>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <el-container>
      <el-header class="header">
        <div class="title">管理员控制台</div>
        <el-button type="danger" size="small" @click="handleLogout">退出登录</el-button>
      </el-header>
      <el-main class="main">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { DataAnalysis, Document, UserFilled } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()

const activeMenu = computed(() => route.path)

const handleLogout = () => {
  localStorage.removeItem('token')
  ElMessage.success('已退出登录')
  router.push({ name: 'login' })
}
</script>

<style scoped>
.layout {
  min-height: 100vh;
}

.aside {
  background: #111827;
  color: #e5e7eb;
  display: flex;
  flex-direction: column;
}

.logo {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 18px;
  color: #f3f4f6;
}

.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #ffffff;
  border-bottom: 1px solid #e5e7eb;
}

.title {
  font-size: 16px;
  font-weight: 600;
}

.main {
  background: #f3f4f6;
}
</style>
