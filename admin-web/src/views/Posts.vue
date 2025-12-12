<template>
  <div class="page">
    <div class="page-header">
      <h2>内容管理</h2>
      <div class="actions">
        <el-select 
          v-model="filterMediaType" 
          placeholder="媒体类型" 
          clearable 
          @change="fetchPosts"
          style="width: 120px; margin-right: 8px"
        >
          <el-option label="全部" value="" />
          <el-option label="图文" value="image" />
          <el-option label="视频" value="video" />
          <el-option label="纯文本" value="text" />
        </el-select>
        
        <el-input
          v-model="searchUserId"
          placeholder="按用户ID过滤"
          clearable
          @clear="fetchPosts"
          @keyup.enter="fetchPosts"
          style="width: 140px; margin-right: 8px"
        />
        <el-button type="primary" plain @click="fetchPosts">刷新</el-button>
      </div>
    </div>

    <el-table v-loading="loading" :data="posts" style="width: 100%">
      <el-table-column prop="id" label="ID" width="80" />
      
      <el-table-column label="用户" width="180">
        <template #default="{ row }">
          <div class="user-cell">
            <el-avatar :size="24" :src="row.user?.avatar_url">{{ (row.user?.username || 'U').charAt(0) }}</el-avatar>
            <span class="username">{{ row.user?.username || `用户#${row.user_id}` }}</span>
          </div>
        </template>
      </el-table-column>

      <el-table-column label="媒体预览" width="100">
        <template #default="{ row }">
          <div v-if="row.media_type === 'image' && row.media_urls.length" class="media-preview">
            <el-image 
              :src="row.media_urls[0]" 
              :preview-src-list="row.media_urls"
              fit="cover"
              class="preview-img"
              preview-teleported
            />
            <div v-if="row.media_urls.length > 1" class="count-badge">+{{ row.media_urls.length - 1 }}</div>
          </div>
          <div v-else-if="row.media_type === 'video' && row.media_urls.length" class="media-preview">
             <div class="video-icon">▶</div>
          </div>
          <span v-else class="text-gray">-</span>
        </template>
      </el-table-column>

      <el-table-column prop="content" label="内容" min-width="200">
        <template #default="{ row }">
          <div class="content-text">{{ truncate(row.content) }}</div>
          <div class="tags-row">
            <el-tag v-for="tag in row.tags" :key="tag.id" size="small" effect="plain" round>
              #{{ tag.name }}
            </el-tag>
          </div>
        </template>
      </el-table-column>

      <el-table-column prop="created_at" label="发布时间" width="160">
        <template #default="{ row }">
          {{ formatDate(row.created_at) }}
        </template>
      </el-table-column>

      <el-table-column label="数据" width="120">
        <template #default="{ row }">
          <div class="stats-cell">
            <span>💬 {{ row.comment_count }}</span>
            <span>⭐ {{ row.average_rating ? row.average_rating.toFixed(1) : '-' }}</span>
          </div>
        </template>
      </el-table-column>

      <el-table-column label="操作" width="100" fixed="right">
        <template #default="{ row }">
          <el-button type="danger" link @click="confirmDelete(row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

import api from '../api'

interface Tag {
  id: number
  name: string
}

interface UserLite {
  id: number
  username: string
  avatar_url?: string
}

interface PostItem {
  id: number
  user_id: number
  content: string
  media_type: string
  media_urls: string[]
  created_at: string
  updated_at: string
  comment_count: number
  average_rating?: number
  tags: Tag[]
  user?: UserLite
}

const posts = ref<PostItem[]>([])
const loading = ref(false)
const searchUserId = ref<string>('')
const filterMediaType = ref<string>('')

const formatDate = (dateStr: string) => new Date(dateStr).toLocaleString()

const truncate = (text: string, length = 60) => {
  if (!text) return ''
  return text.length > length ? `${text.slice(0, length)}...` : text
}

const fetchPosts = async () => {
  loading.value = true
  try {
    const params: Record<string, any> = {}
    if (searchUserId.value) params.user_id = searchUserId.value
    if (filterMediaType.value) params.media_type = filterMediaType.value
    
    const res = await api.get<PostItem[]>('/posts', { params })
    posts.value = res.data
  } catch (error: any) {
    const detail = error?.response?.data?.detail || '获取内容列表失败'
    ElMessage.error(detail)
  } finally {
    loading.value = false
  }
}

const confirmDelete = (postId: number) => {
  ElMessageBox.confirm('确认删除该内容吗？', '提示', { type: 'warning' })
    .then(() => deletePost(postId))
    .catch(() => {})
}

const deletePost = async (postId: number) => {
  try {
    await api.delete(`/posts/${postId}`)
    ElMessage.success('删除成功')
    await fetchPosts()
  } catch (error: any) {
    const detail = error?.response?.data?.detail || '删除失败'
    ElMessage.error(detail)
  }
}

onMounted(fetchPosts)
</script>

<style scoped>
.page {
  background: var(--c-white);
  padding: 24px;
  border-radius: 12px;
  border: var(--border-thick);
  box-shadow: var(--shadow-hard);
}

.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 24px;
}

.page-header h2 {
  font-weight: 900;
  letter-spacing: 0.5px;
}

.actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

:deep(.el-table) {
  border: 1px solid var(--c-black);
  box-shadow: var(--shadow-hard);
}

:deep(.el-table th.el-table__cell) {
  background: var(--c-black);
  color: var(--c-white);
  font-weight: 900;
  border: 1px solid var(--c-black);
}

:deep(.el-table td.el-table__cell) {
  border: 1px solid var(--c-black);
}

.user-cell {
  display: flex;
  align-items: center;
  gap: 8px;
}

.username {
  font-size: 14px;
  color: #374151;
}

.media-preview {
  position: relative;
  width: 40px;
  height: 40px;
  border-radius: 4px;
  overflow: hidden;
  background: #f3f4f6;
  display: flex;
  align-items: center;
  justify-content: center;
}

.preview-img {
  width: 100%;
  height: 100%;
}

.count-badge {
  position: absolute;
  bottom: 0;
  right: 0;
  background: rgba(0,0,0,0.6);
  color: white;
  font-size: 10px;
  padding: 0 4px;
  border-top-left-radius: 4px;
}

.video-icon {
  color: #9ca3af;
  font-size: 12px;
}

.text-gray {
  color: #d1d5db;
}

.content-text {
  font-size: 14px;
  color: #1f2937;
  margin-bottom: 4px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.tags-row {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.stats-cell {
  display: flex;
  flex-direction: column;
  gap: 2px;
  font-size: 12px;
  color: #6b7280;
}
</style>
