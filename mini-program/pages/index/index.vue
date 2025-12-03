<template>
  <view class="page">
    <view class="tabs-container">
      <view class="tabs">
        <view
          v-for="tab in tabs"
          :key="tab.value"
          :class="['tab', selectedTab === tab.value ? 'active' : '']"
          @click="switchTab(tab.value)"
        >
          <text class="tab-text">{{ tab.label }}</text>
          <view class="tab-line" v-if="selectedTab === tab.value"></view>
        </view>
      </view>
    </view>

    <scroll-view
      scroll-y
      class="feed"
      :lower-threshold="80"
      @scrolltolower="loadMore"
      refresher-enabled
      :refresher-triggered="refreshing"
      @refresherrefresh="refresh"
    >
      <view class="feed-content">
        <view v-for="item in posts" :key="item.id">
          <PostCard :post="item" :currentUserId="currentUserId" @like="onLike" @comment="onComment" @delete="onDelete" />
        </view>
        <view class="empty" v-if="!loading && posts.length === 0">
          <image class="empty-img" src="https://img.alicdn.com/imgextra/i2/O1CN01d159be1k2AII0fV6o_!!6000000004624-2-tps-200-200.png" mode="aspectFit" />
          <text>暂无动态</text>
        </view>
        <view class="loading" v-if="loading">
          <text class="loading-text">加载中...</text>
        </view>
      </view>
    </scroll-view>

    <view class="fab" @click="goUpload">
      <text class="fab-icon">＋</text>
    </view>
  </view>
</template>

<script setup>
import { ref } from 'vue'
import { onMounted } from 'vue'
import { onReachBottom } from '@dcloudio/uni-app'
import PostCard from '../../components/PostCard.vue'
import { get } from '../../utils/request'

const posts = ref([])
const skip = ref(0)
const limit = 10
const loading = ref(false)
const finished = ref(false)
const refreshing = ref(false)
const currentUserId = ref(null)
const selectedTab = ref('all')
const tabs = [
  { label: '推荐', value: 'all' },
  { label: '关注', value: 'following' },
]

const fetchPosts = async (append = false) => {
  if (loading.value || finished.value) return
  loading.value = true
  try {
    const params = { skip: skip.value, limit }
    if (selectedTab.value === 'following') {
      params.filter = 'following'
    }
    const res = await get('/posts', params)
    const list = Array.isArray(res) ? res : []
    if (append) {
      posts.value = posts.value.concat(list)
    } else {
      posts.value = list
    }
    if (list.length < limit) {
      finished.value = true
    } else {
      skip.value += limit
    }
  } catch (err) {
    console.error(err)
    const detail = err?.data?.detail || '加载失败'
    uni.showToast({ title: detail, icon: 'none' })
    if (selectedTab.value === 'following') {
      selectedTab.value = 'all'
      skip.value = 0
      finished.value = false
      fetchPosts(false)
    }
  } finally {
    loading.value = false
    refreshing.value = false
  }
}

const refresh = () => {
  refreshing.value = true
  skip.value = 0
  finished.value = false
  fetchPosts(false)
}

const switchTab = (tab) => {
  if (selectedTab.value === tab) return
  selectedTab.value = tab
  skip.value = 0
  finished.value = false
  posts.value = []
  fetchPosts(false)
}

const loadMore = () => {
  if (!finished.value) {
    fetchPosts(true)
  }
}

const goUpload = () => {
  uni.navigateTo({ url: '/pages/upload/upload' })
}

const onLike = (post) => {
  // PostCard handles the API call and toast
}

const onComment = ({ post, content }) => {
  // PostCard handles the API call and toast
}

const onDelete = (postId) => {
  posts.value = posts.value.filter(p => p.id !== postId)
}

const fetchProfile = async () => {
  try {
    const res = await get('/auth/me')
    currentUserId.value = res?.id || null
  } catch (err) {
    currentUserId.value = null
  }
}

onMounted(() => {
  fetchProfile()
  fetchPosts()
})

onReachBottom(() => {
  loadMore()
})
</script>

<style scoped>
.page {
  height: 100vh;
  background: #f8f8f8;
  display: flex;
  flex-direction: column;
}

.tabs-container {
  background: #ffffff;
  padding-top: 10rpx;
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: 0 2rpx 10rpx rgba(0,0,0,0.02);
}

.tabs {
  display: flex;
  justify-content: center;
  gap: 60rpx;
}

.tab {
  padding: 20rpx 0;
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.tab-text {
  font-size: 32rpx;
  color: #9ca3af;
  font-weight: 500;
  transition: all 0.3s;
}

.tab.active .tab-text {
  color: #1f2937;
  font-weight: 700;
  font-size: 34rpx;
}

.tab-line {
  width: 40rpx;
  height: 6rpx;
  background: #07c160;
  border-radius: 6rpx;
  position: absolute;
  bottom: 10rpx;
}

.feed {
  flex: 1;
  height: 0; /* Important for scroll-view in flex container */
}

.feed-content {
  padding: 24rpx;
  padding-bottom: 160rpx;
}

.fab {
  position: fixed;
  right: 40rpx;
  bottom: 60rpx;
  width: 110rpx;
  height: 110rpx;
  background: linear-gradient(135deg, #07c160, #059669);
  color: #ffffff;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 12rpx 30rpx rgba(7, 193, 96, 0.4);
  transition: transform 0.1s;
}

.fab:active {
  transform: scale(0.95);
}

.fab-icon {
  font-size: 60rpx;
  font-weight: 300;
  margin-top: -6rpx;
}

.loading,
.empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60rpx 0;
  color: #9ca3af;
  gap: 20rpx;
}

.empty-img {
  width: 200rpx;
  height: 200rpx;
  opacity: 0.5;
}

.loading-text {
  font-size: 26rpx;
}
</style>
