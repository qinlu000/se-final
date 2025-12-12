<template>
  <el-container class="layout">
    <el-aside width="200px" class="aside">
      <div class="logo">Moments Admin</div>
      <el-menu
        router
        :default-active="activeMenu"
        background-color="#000000"
        text-color="#ffffff"
        active-text-color="#000000"
        class="menu"
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
:global(:root) {
  --c-black: #000000;
  --c-white: #ffffff;
  --c-yellow: #ffe600;
  --c-pink: #ff6b6b;
  --border-thick: 2px solid var(--c-black);
  --shadow-hard: 8px 8px 0px var(--c-black);
  --radius-m: 12px;
}

.layout {
  min-height: 100vh;
}

.aside {
  background: var(--c-black);
  color: #ffffff;
  display: flex;
  flex-direction: column;
  border-right: var(--border-thick);
}

.logo {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 18px;
  color: var(--c-white);
  border-bottom: var(--border-thick);
}

.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: var(--c-white);
  border-bottom: var(--border-thick);
  box-shadow: var(--shadow-hard);
  padding-right: 16px;
}

.title {
  font-size: 16px;
  font-weight: 600;
}

.main {
  background: #f3f3f3;
  padding: 16px;
}

:deep(.menu) {
  border-right: none;
}

:deep(.menu .el-menu-item) {
  font-weight: 800;
  height: 56px;
}

:deep(.menu .el-menu-item.is-active) {
  background: var(--c-yellow) !important;
  color: var(--c-black) !important;
  border: 2px solid var(--c-yellow);
  box-shadow: 4px 4px 0px var(--c-black);
  border-radius: 10px;
}

</style>
