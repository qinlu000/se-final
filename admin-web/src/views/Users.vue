<template>
  <div class="page">
    <div class="page-header">
      <h2>用户管理</h2>
      <div class="actions">
        <el-input
          v-model="searchQuery"
          placeholder="搜索用户名/昵称"
          prefix-icon="Search"
          clearable
          @clear="fetchUsers"
          @keyup.enter="fetchUsers"
          style="width: 240px; margin-right: 12px"
        />
        <el-button type="primary" plain @click="fetchUsers">刷新</el-button>
      </div>
    </div>

    <el-table v-loading="loading" :data="users" style="width: 100%">
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column label="用户" width="240">
        <template #default="{ row }">
          <div class="user-cell">
            <el-avatar :size="32" :src="row.avatar_url">{{ row.username.charAt(0).toUpperCase() }}</el-avatar>
            <div class="user-info">
              <div class="username">{{ row.username }}</div>
              <div class="nickname">{{ row.nickname }}</div>
            </div>
          </div>
        </template>
      </el-table-column>
      <el-table-column label="管理员" width="100">
        <template #default="{ row }">
          <el-tag :type="row.is_admin ? 'success' : 'info'" effect="light" round>
            {{ row.is_admin ? '管理员' : '普通用户' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="注册时间">
        <template #default="{ row }">
          {{ formatDate(row.created_at) }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="120" fixed="right">
        <template #default="{ row }">
          <el-button 
            type="danger" 
            link 
            :disabled="row.is_admin"
            @click="confirmDelete(row.id)"
          >
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search } from '@element-plus/icons-vue'

import api from '../api'

interface UserItem {
  id: number
  username: string
  nickname?: string
  avatar_url?: string
  is_admin: boolean
  created_at: string
}

const users = ref<UserItem[]>([])
const loading = ref(false)
const searchQuery = ref('')

const formatDate = (dateStr: string) => {
  return new Date(dateStr).toLocaleString()
}

const fetchUsers = async () => {
  loading.value = true
  try {
    const params: any = {}
    if (searchQuery.value) params.search = searchQuery.value
    
    const res = await api.get<UserItem[]>('/users', { params })
    users.value = res.data
  } catch (error: any) {
    const detail = error?.response?.data?.detail || '获取用户列表失败'
    ElMessage.error(detail)
  } finally {
    loading.value = false
  }
}

const confirmDelete = (userId: number) => {
  ElMessageBox.confirm('确认删除该用户吗？此操作不可逆！', '警告', {
    confirmButtonText: '确定删除',
    cancelButtonText: '取消',
    type: 'warning',
  })
    .then(() => deleteUser(userId))
    .catch(() => {})
}

const deleteUser = async (userId: number) => {
  try {
    await api.delete(`/users/${userId}`)
    ElMessage.success('删除成功')
    await fetchUsers()
  } catch (error: any) {
    const detail = error?.response?.data?.detail || '删除失败'
    ElMessage.error(detail)
  }
}

onMounted(fetchUsers)
</script>

<style scoped>
.page {
  background: #ffffff;
  padding: 24px;
  border-radius: 12px;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
}

.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 24px;
}

.actions {
  display: flex;
  align-items: center;
}

.user-cell {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-info {
  display: flex;
  flex-direction: column;
  line-height: 1.2;
}

.username {
  font-weight: 500;
  color: #111827;
}

.nickname {
  font-size: 12px;
  color: #6b7280;
}
</style>
