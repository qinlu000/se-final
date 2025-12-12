<template>
  <view class="card neu-card">
    <view class="header">
      <image class="avatar" :src="post.user?.avatar_url || defaultAvatar" mode="aspectFill" />
      <view class="info">
        <view class="name-row">
          <text class="name">{{ post.user?.nickname || post.user?.username || '匿名用户' }}</text>
          <view
            v-if="showFollowButton"
            class="follow-btn"
            :class="{ active: isFollowing }"
            @click.stop="toggleFollow"
          >
            {{ isFollowing ? '已关注' : '关注' }}
          </view>
        </view>
        <text class="time">{{ formatTime(post.created_at) }}</text>
      </view>
      <view v-if="post.user_id === currentUserId" class="delete-btn" @click.stop="deletePost">
        ✕
      </view>
    </view>

    <view class="content">{{ post.content }}</view>

    <MediaGrid v-if="post.media_urls?.length" :media="post.media_urls" />

    <view class="footer">
      <view class="action-pill" :class="{ active: isLiked }" @click.stop="emitLike">
        <text class="icon">{{ isLiked ? '♥' : '♡' }}</text>
        <text class="count">{{ isLiked ? '已赞' : '点赞' }}</text>
      </view>
      <view class="action-pill" @click.stop="openComment">
        <text class="icon">💬</text>
        <text class="count">{{ localComments.length > 0 ? localComments.length : '评论' }}</text>
      </view>
    </view>

    <!-- Comments List -->
    <view v-if="localComments.length > 0" class="comments-list">
      <view v-for="(comment, index) in localComments" :key="index" class="comment-item">
        <text class="comment-user">{{ comment.user?.nickname || comment.user?.username || '我' }}: </text>
        <text class="comment-content">{{ comment.content }}</text>
      </view>
    </view>

    <view v-if="showCommentInput" class="comment-input-area">
      <input
        v-model="commentText"
        class="input"
        placeholder="写下你的评论..."
        confirm-type="send"
        @confirm="submitComment"
        focus
      />
      <button class="send-btn neu-btn" @click="submitComment">发送</button>
    </view>
  </view>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { request } from '../utils/request'
import MediaGrid from './MediaGrid.vue'

const emit = defineEmits(['like', 'comment', 'delete'])
const props = defineProps({
  post: {
    type: Object,
    required: true,
  },
  currentUserId: {
    type: Number,
    default: null,
  },
})

const showCommentInput = ref(false)
const commentText = ref('')
const defaultAvatar =
  'https://img.alicdn.com/imgextra/i3/O1CN01G9FphX1s2oAtxEvsN_!!6000000005714-2-tps-200-200.png'
const isFollowing = ref(props.post?.is_following || false)
const isLiked = ref(props.post?.is_liked || false)
const localComments = ref(props.post?.comments || [])

const showFollowButton = computed(() => {
  if (!props.post?.user_id || !props.currentUserId) return false
  return props.post.user_id !== props.currentUserId
})

watch(
  () => props.post,
  (newVal) => {
    if (newVal) {
      isFollowing.value = !!newVal.is_following
      isLiked.value = !!newVal.is_liked
      // If backend sends comments, sync them. If not, keep local or empty.
      if (newVal.comments) {
        localComments.value = newVal.comments
      }
    }
  },
  { deep: true, immediate: true }
)

const emitLike = async () => {
  // Optimistic update
  const originalState = isLiked.value
  isLiked.value = !isLiked.value
  
  try {
    if (originalState) {
       // Was liked, now unliked -> Call DELETE
       await request({
          url: `/posts/${props.post.id}/rate`,
          method: 'DELETE'
       })
       uni.showToast({ title: '已取消', icon: 'none' })
    } else {
       // Was not liked, now liked -> Call POST
       await request({
          url: `/posts/${props.post.id}/rate`,
          method: 'POST',
          data: { score: 5 }
       })
       uni.showToast({ title: '已点赞', icon: 'success' })
    }
    
    emit('like', props.post)
  } catch (err) {
    console.error(err)
    isLiked.value = originalState // Revert on error
    uni.showToast({ title: '操作失败', icon: 'none' })
  }
}

const openComment = () => {
  showCommentInput.value = !showCommentInput.value
}

const submitComment = async () => {
  if (!commentText.value.trim()) return
  
  const content = commentText.value
  const newComment = {
    user: { nickname: '我' },
    content: content
  }
  localComments.value.push(newComment)
  commentText.value = ''
  showCommentInput.value = false

  try {
    await request({
      url: `/posts/${props.post.id}/comments`,
      method: 'POST',
      data: { content }
    })
    uni.showToast({ title: '评论成功', icon: 'success' })
    emit('comment', { post: props.post, content })
  } catch (err) {
    console.error(err)
    localComments.value.pop()
    uni.showToast({ title: '评论失败', icon: 'none' })
  }
}

const toggleFollow = async () => {
  if (!props.post?.user_id) return
  const targetId = props.post.user_id
  
  // Optimistic update
  const originalState = isFollowing.value
  isFollowing.value = !isFollowing.value
  
  try {
    if (originalState) {
      await request({ url: `/users/${targetId}/follow`, method: 'DELETE' })
      uni.showToast({ title: '已取消关注', icon: 'none' })
    } else {
      await request({ url: `/users/${targetId}/follow`, method: 'POST' })
      uni.showToast({ title: '已关注', icon: 'success' })
    }
  } catch (err) {
    console.error(err)
    isFollowing.value = originalState
    uni.showToast({ title: '操作失败', icon: 'none' })
  }
}

const deletePost = () => {
  uni.showModal({
    title: '提示',
    content: '确定要删除这条动态吗？',
    success: async (res) => {
      if (res.confirm) {
        try {
          await request({ url: `/posts/${props.post.id}`, method: 'DELETE' })
          uni.showToast({ title: '已删除', icon: 'success' })
          emit('delete', props.post.id)
        } catch (err) {
          console.error(err)
          uni.showToast({ title: '删除失败', icon: 'none' })
        }
      }
    }
  })
}

const formatTime = (timeStr) => {
  if (!timeStr) return ''
  const date = new Date(timeStr)
  const now = new Date()
  const diff = now - date
  
  if (diff < 60000) return '刚刚'
  if (diff < 3600000) return `${Math.floor(diff / 60000)}分钟前`
  if (diff < 86400000) return `${Math.floor(diff / 3600000)}小时前`
  
  return `${date.getMonth() + 1}-${date.getDate()}`
}
</script>

<style scoped>
.card {
  padding: 32rpx;
  margin: 20rpx 8rpx 28rpx;
  border-radius: var(--radius-m);
}

.header {
  display: flex;
  align-items: flex-start;
  margin-bottom: 24rpx;
  gap: 20rpx;
}

.avatar {
  width: 96rpx;
  height: 96rpx;
  border-radius: 50%;
  border: var(--border-thick);
  background: var(--c-white);
  box-shadow: var(--shadow-hard);
}

.info {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  min-height: 96rpx;
}

.name-row {
  display: flex;
  align-items: center;
  gap: 12rpx;
  margin-bottom: 6rpx;
}

.name {
  font-size: 32rpx;
  font-weight: 800;
  letter-spacing: 0.6rpx;
}

.time {
  font-size: 24rpx;
  color: #6b7280;
}

.follow-btn {
  font-size: 22rpx;
  padding: 6rpx 18rpx;
  border-radius: var(--radius-full);
  border: var(--border-thick);
  background: var(--c-cyan);
  font-weight: 700;
  box-shadow: var(--shadow-hard);
}

.follow-btn.active {
  background: #ffffff;
}

.delete-btn {
  margin-left: 12rpx;
  font-size: 32rpx;
  padding: 10rpx;
  color: #111;
}

.content {
  font-size: 32rpx;
  line-height: 1.7;
  margin-bottom: 16rpx;
  letter-spacing: 0.5rpx;
}

.footer {
  display: flex;
  align-items: center;
  margin-top: 24rpx;
  gap: 24rpx;
  flex-wrap: wrap;
}

.action-pill {
  display: inline-flex;
  align-items: center;
  gap: 10rpx;
  padding: 12rpx 22rpx;
  border-radius: var(--radius-full);
  border: var(--border-thick);
  background: var(--c-white);
  box-shadow: var(--shadow-hard);
  font-weight: 700;
  color: var(--c-black);
  transition: transform 0.08s ease, box-shadow 0.08s ease, background 0.08s ease;
}

.action-pill:active {
  box-shadow: none;
  transform: translate(4rpx, 4rpx);
}

.action-pill.active {
  background: var(--c-pink);
  color: var(--c-black);
}

.icon {
  font-size: 36rpx;
}

.action-pill.active .icon {
  animation: like-pop 0.18s ease;
}

.count {
  font-size: 26rpx;
}

.comments-list {
  margin-top: 28rpx;
  padding: 22rpx;
  border: var(--border-thick);
  border-radius: var(--radius-m);
  background: #ffffff;
  box-shadow: var(--shadow-hard);
}

.comment-item {
  font-size: 28rpx;
  margin-bottom: 12rpx;
  line-height: 1.5;
}

.comment-item:last-child {
  margin-bottom: 0;
}

.comment-user {
  font-weight: 800;
}

.comment-content {
  color: #1f2937;
}

.comment-input-area {
  margin-top: 24rpx;
  display: flex;
  gap: 16rpx;
  align-items: center;
}

.input {
  flex: 1;
  height: 76rpx;
  background: #ffffff;
  border-radius: 38rpx;
  padding: 0 30rpx;
  font-size: 28rpx;
  border: var(--border-thick);
  box-shadow: var(--shadow-hard);
}

.send-btn {
  font-size: 28rpx;
  padding: 0 32rpx;
  height: 76rpx;
  line-height: 76rpx;
  margin: 0;
}

:deep(.media-grid) {
  margin-top: 14rpx;
}

:deep(.media-item) {
  border: var(--border-thick);
  border-radius: var(--radius-m);
  overflow: hidden;
  box-shadow: var(--shadow-hard);
}

@keyframes like-pop {
  0% {
    transform: scale(1);
  }
  70% {
    transform: scale(1.5);
  }
  100% {
    transform: scale(1);
  }
}
</style>
