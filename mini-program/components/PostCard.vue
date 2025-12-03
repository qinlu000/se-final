<template>
  <view class="card">
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
      <view class="action-item" @click.stop="emitLike">
        <text class="icon" :class="{ liked: isLiked }">{{ isLiked ? '♥' : '♡' }}</text>
        <text class="count" :class="{ liked: isLiked }">{{ isLiked ? '已赞' : '点赞' }}</text>
      </view>
      <view class="action-item" @click.stop="openComment">
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
      <button class="send-btn" @click="submitComment">发送</button>
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
  background: #ffffff;
  padding: 30rpx;
  border-radius: 16rpx;
  margin-bottom: 20rpx;
  box-shadow: 0 2rpx 12rpx rgba(0, 0, 0, 0.03);
}

.header {
  display: flex;
  align-items: flex-start;
  margin-bottom: 20rpx;
}

.avatar {
  width: 80rpx;
  height: 80rpx;
  border-radius: 50%;
  margin-right: 20rpx;
  background: #f3f4f6;
}

.info {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  min-height: 80rpx;
}

.name-row {
  display: flex;
  align-items: center;
  gap: 12rpx;
  margin-bottom: 4rpx;
}

.name {
  font-size: 30rpx;
  font-weight: 600;
  color: #333;
}

.time {
  font-size: 24rpx;
  color: #9ca3af;
}

.follow-btn {
  font-size: 22rpx;
  color: #07c160;
  background: rgba(7, 193, 96, 0.1);
  padding: 4rpx 16rpx;
  border-radius: 20rpx;
  font-weight: 500;
}

.follow-btn.active {
  background: #f3f4f6;
  color: #9ca3af;
}

.delete-btn {
  margin-left: 16rpx;
  color: #d1d5db;
  font-size: 28rpx;
  padding: 10rpx;
}

.content {
  font-size: 32rpx;
  color: #1f2937;
  line-height: 1.6;
  margin-bottom: 20rpx;
  letter-spacing: 0.5rpx;
}

.footer {
  display: flex;
  align-items: center;
  margin-top: 24rpx;
  gap: 40rpx;
}

.action-item {
  display: flex;
  align-items: center;
  gap: 8rpx;
  color: #6b7280;
}

.icon {
  font-size: 36rpx;
  transition: all 0.2s;
}

.icon.liked {
  color: #ef4444;
  transform: scale(1.1);
}

.count {
  font-size: 26rpx;
}

.count.liked {
  color: #ef4444;
}

.comments-list {
  margin-top: 24rpx;
  background: #f9fafb;
  padding: 20rpx;
  border-radius: 12rpx;
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
  font-weight: 600;
  color: #374151;
}

.comment-content {
  color: #4b5563;
}

.comment-input-area {
  margin-top: 24rpx;
  display: flex;
  gap: 16rpx;
  align-items: center;
}

.input {
  flex: 1;
  height: 72rpx;
  background: #f3f4f6;
  border-radius: 36rpx;
  padding: 0 30rpx;
  font-size: 28rpx;
}

.send-btn {
  font-size: 28rpx;
  background: #07c160;
  color: white;
  padding: 0 32rpx;
  height: 72rpx;
  line-height: 72rpx;
  border-radius: 36rpx;
  margin: 0;
}
</style>
