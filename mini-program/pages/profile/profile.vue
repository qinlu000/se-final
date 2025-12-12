<template>
  <view class="page">
    <view class="header-bg neu-card">
      <view class="settings-btn" @click="handleLogout">
        <text class="settings-icon">⚙️</text>
      </view>
    </view>
    
    <view class="profile-card neu-card">
      <view class="avatar-container">
        <image class="avatar" :src="profile.avatar_url || defaultAvatar" mode="aspectFill" />
      </view>
      <view class="info">
        <text class="name">{{ profile.nickname || profile.username || '未登录' }}</text>
        <text class="sub">加入时间：{{ formatDate(profile.created_at) }}</text>
        <view class="edit-btn neu-btn" @click="goEditProfile">
          <text>编辑资料</text>
        </view>
      </view>
      
      <view class="stats-row">
        <view class="stat-item" hover-class="stat-hover">
          <text class="stat-num">{{ followingCount }}</text>
          <text class="stat-label">关注</text>
        </view>
        <view class="stat-divider"></view>
        <view class="stat-item" hover-class="stat-hover">
          <text class="stat-num">{{ followerCount }}</text>
          <text class="stat-label">粉丝</text>
        </view>
        <view class="stat-divider"></view>
        <view class="stat-item" hover-class="stat-hover">
          <text class="stat-num">{{ myPosts.length }}</text>
          <text class="stat-label">动态</text>
        </view>
      </view>
    </view>

    <view class="section">
      <view class="section-header">
        <text class="section-title">我的动态</text>
      </view>
      <view class="post-list">
        <view v-for="item in myPosts" :key="item.id">
          <PostCard :post="item" :currentUserId="profile.id" @like="onLike" @comment="onComment" @delete="onDelete" />
        </view>
      </view>
      <view class="empty" v-if="myPosts.length === 0">
        <image class="empty-img" src="https://img.alicdn.com/imgextra/i2/O1CN01d159be1k2AII0fV6o_!!6000000004624-2-tps-200-200.png" mode="aspectFit" />
        <text>暂无动态，快去发布第一条吧</text>
      </view>
    </view>
  </view>
</template>

<script setup>
import { reactive, ref, onMounted } from 'vue'
import PostCard from '../../components/PostCard.vue'
import { get } from '../../utils/request'

const profile = reactive({
  id: null,
  username: '',
  nickname: '',
  avatar_url: '',
  created_at: '',
})
const myPosts = ref([])
const followerCount = ref(0)
const followingCount = ref(0)
const defaultAvatar =
  'https://img.alicdn.com/imgextra/i3/O1CN01G9FphX1s2oAtxEvsN_!!6000000005714-2-tps-200-200.png'

const fetchProfile = async () => {
  try {
    const res = await get('/auth/me')
    Object.assign(profile, res || {})
  } catch (err) {
    console.error(err)
    uni.showToast({ title: '请先登录', icon: 'none' })
    setTimeout(() => {
      uni.reLaunch({ url: '/pages/login/login' })
    }, 1500)
  }
}

const fetchMyPosts = async () => {
  if (!profile.id) return
  try {
    const res = await get('/posts', { user_id: profile.id })
    myPosts.value = Array.isArray(res) ? res : []
  } catch (err) {
    console.error(err)
  }
}

const fetchFollowCounts = async () => {
  if (!profile.id) return
  try {
    const followers = await get(`/users/${profile.id}/followers`)
    const following = await get(`/users/${profile.id}/following`)
    followerCount.value = Array.isArray(followers) ? followers.length : 0
    followingCount.value = Array.isArray(following) ? following.length : 0
  } catch (err) {
    console.error(err)
  }
}

const formatDate = (str) => {
  if (!str) return ''
  const d = new Date(str)
  return `${d.getFullYear()}-${d.getMonth() + 1}-${d.getDate()}`
}

const onLike = () => {}
const onComment = () => {}
const onDelete = (postId) => {
  myPosts.value = myPosts.value.filter(p => p.id !== postId)
}

const handleLogout = () => {
  uni.showModal({
    title: '提示',
    content: '确定要退出登录吗？',
    success: (res) => {
      if (res.confirm) {
        uni.removeStorageSync('token')
        uni.reLaunch({ url: '/pages/login/login' })
      }
    }
  })
}

const goEditProfile = () => {
  uni.showToast({ title: '功能开发中...', icon: 'none' })
}

onMounted(async () => {
  await fetchProfile()
  await fetchMyPosts()
  await fetchFollowCounts()
})
</script>

<style scoped>
.page {
  min-height: 100vh;
  background-color: var(--c-bg);
  background-image: radial-gradient(#dcdcdc 1px, transparent 1px);
  background-size: 18px 18px;
  padding-bottom: 40rpx;
}

.header-bg {
  height: 320rpx;
  background: var(--c-white);
  border: var(--border-thick);
  box-shadow: var(--shadow-hard);
  border-radius: 0 0 var(--radius-m) var(--radius-m);
  position: relative;
}

.settings-btn {
  position: absolute;
  top: 100rpx; /* Adjust for status bar */
  right: 40rpx;
  width: 72rpx;
  height: 72rpx;
  background: var(--c-yellow);
  border: var(--border-thick);
  border-radius: var(--radius-m);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: var(--shadow-hard);
}

.settings-icon {
  font-size: 32rpx;
}

.profile-card {
  margin: -120rpx 30rpx 0;
  background: var(--c-white);
  border-radius: var(--radius-m);
  padding: 0 40rpx 50rpx;
  border: var(--border-thick);
  box-shadow: var(--shadow-hard);
  display: flex;
  flex-direction: column;
  align-items: center;
}

.avatar-container {
  margin-top: -70rpx;
  padding: 12rpx;
  background: var(--c-white);
  border-radius: 50%;
  border: var(--border-thick);
  box-shadow: var(--shadow-hard);
}

.avatar {
  width: 140rpx;
  height: 140rpx;
  border-radius: 50%;
  display: block;
}

.info {
  text-align: center;
  margin-top: 24rpx;
  margin-bottom: 48rpx;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.name {
  font-size: 44rpx;
  font-weight: 700;
  color: var(--c-black);
  display: block;
  margin-bottom: 8rpx;
}

.sub {
  font-size: 24rpx;
  color: #4b5563;
  margin-bottom: 24rpx;
}

.edit-btn {
  padding: 14rpx 36rpx;
  font-size: 26rpx;
  border-radius: var(--radius-full);
  box-shadow: var(--shadow-hard);
}

.stats-row {
  display: flex;
  width: 100%;
  justify-content: space-between;
  align-items: center;
  padding: 0 20rpx;
  margin-top: 10rpx;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 14rpx 20rpx;
  min-width: 140rpx;
  gap: 6rpx;
  font-weight: 800;
}

.stat-num {
  font-size: 40rpx;
  font-weight: 800;
  color: var(--c-black);
  margin-bottom: 4rpx;
}

.stat-label {
  font-size: 24rpx;
  color: #374151;
  font-weight: 700;
}

.stat-hover {
  background: #fff7a6;
}

.stat-divider {
  width: 2rpx;
  height: 76rpx;
  background: var(--c-black);
}

.section {
  margin-top: 40rpx;
  padding: 0 30rpx;
}

.section-header {
  margin-bottom: 24rpx;
  display: flex;
  align-items: center;
}

.section-title {
  font-size: 34rpx;
  font-weight: 700;
  color: var(--c-black);
}

.empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80rpx 0;
  color: #9ca3af;
  gap: 20rpx;
}

.empty-img {
  width: 200rpx;
  height: 200rpx;
  opacity: 0.5;
}
</style>
