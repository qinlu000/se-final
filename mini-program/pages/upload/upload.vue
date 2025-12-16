<template>
  <view class="page">
    <!-- Navbar placeholder (if needed) or simple title -->
    <!-- <view class="top-bar">
      <text class="title">发布动态</text>
    </view> -->

    <view class="input-section neu-card">
      <textarea
        v-model="content"
        class="main-input"
        placeholder="分享这一刻的想法..."
        placeholder-style="color: #9ca3af; font-weight: 500;"
        :maxlength="1000"
        auto-height
        show-confirm-bar
      />
      
      <view class="tools-row">
        <view class="word-count" :class="{ warning: content.length > 450 }">
          {{ content.length }}/1000
        </view>
        <button class="neu-btn ai-btn" @click="openMagicCompose">
          <text>🪄 AI 帮写</text>
        </button>
      </view>
    </view>

    <view class="tags-section neu-card">
      <view class="section-title-sm">
        <text>添加话题</text>
        <text class="limit-hint">{{ tags.length }}/5</text>
      </view>
      <view class="input-row">
        <text class="hash-icon">#</text>
        <input 
          v-model="currentTag" 
          class="tag-input" 
          placeholder="添加标签 (回车添加)" 
          confirm-type="done"
          @confirm="addTag"
        />
        <view class="add-btn-mini" @click="addTag">＋</view>
      </view>
      
      <view v-if="tags.length > 0" class="tags-list">
        <view v-for="tag in tags" :key="tag" class="tag-pill" @click="removeTag(tag)">
          <text>#{{ tag }}</text>
          <text class="close">×</text>
        </view>
      </view>
    </view>

    <view class="media-section">
      <view class="section-title">
        <text>多媒体</text>
        <text class="limit-hint">{{ images.length }}/9</text>
      </view>
      
      <view class="picker-grid">
        <view v-for="(img, idx) in images" :key="idx" class="img-box neu-card-sm">
          <image :src="img" mode="aspectFill" />
          <view class="remove-btn" @click="removeImage(idx)">✕</view>
        </view>
        
        <view v-if="video" class="img-box neu-card-sm">
           <video :src="video" class="preview-video" :controls="false" :show-center-play-btn="false"></video>
           <view class="remove-btn" @click="removeVideo">✕</view>
        </view>

        <view v-if="images.length < 9 && !video" class="add-box" @click="chooseImages">
          <text class="plus-icon">＋</text>
        </view>
      </view>
    </view>

    <view class="footer-action">
      <button class="post-btn neu-btn-lg" :disabled="submitting" @click="submitPost">
        {{ submitting ? '发布中...' : '发布此刻' }}
      </button>
    </view>
  
    <NeuPopup 
      v-model:visible="showAiSheet"
      type="sheet"
      title="✨ AI 魔法助手"
      :actions="aiActions"
      @action="onAiAction"
    />
  </view>
</template>

<script setup>
import { ref } from 'vue'
import { post, BASE_URL } from '../../utils/request'
import { askAI } from '../../api/ai'
import NeuPopup from '../../components/NeuPopup.vue'

const content = ref('')
const images = ref([])
const video = ref('')
const tags = ref([]) // Array of strings
const currentTag = ref('')
const submitting = ref(false)
const aiLoading = ref(false)
const showAiSheet = ref(false)
const aiActions = ['🪄 润色内容', '😀 添加 Emoji', '🏷️ 生成标题']

const addTag = () => {
  const val = currentTag.value.trim()
  if (!val) return
  if (tags.value.length >= 5) {
    uni.showToast({ title: '最多添加5个标签', icon: 'none' })
    return
  }
  if (tags.value.includes(val)) {
    uni.showToast({ title: '标签已存在', icon: 'none' })
    return
  }
  tags.value.push(val)
  currentTag.value = ''
}

const removeTag = (t) => {
  tags.value = tags.value.filter(item => item !== t)
}

const chooseImages = () => {
  if (video.value) {
    uni.showToast({ title: '视频和图片不能同时上传', icon: 'none' })
    return
  }
  uni.showActionSheet({
    itemList: ['图片', '视频'],
    success: (res) => {
      if (res.tapIndex === 0) {
        uni.chooseImage({
          count: 9 - images.value.length,
          sizeType: ['compressed'],
          success: (r) => {
            images.value = images.value.concat(r.tempFilePaths)
          },
        })
      } else {
        uni.chooseVideo({
          sourceType: ['camera', 'album'],
          compressed: true,
          maxDuration: 60,
          success: (r) => {
            video.value = r.tempFilePath
            images.value = [] // Clear images if video selected
          }
        })
      }
    }
  })
}

const removeImage = (idx) => {
  images.value.splice(idx, 1)
}

const removeVideo = () => {
  video.value = ''
}

const handleMagicResult = async (mode) => {
  if (!content.value.trim()) {
    uni.showToast({ title: '先写点内容吧', icon: 'none' })
    return
  }
  aiLoading.value = true
  uni.showLoading({ title: 'AI生成中...', mask: true })
  try {
    const res = await askAI({ content: content.value, mode })
    if (res?.status === 'sensitive') {
      uni.showToast({ title: '内容包含敏感信息', icon: 'none' })
      return
    }
    if (mode === 'title' && res?.suggestions?.length) {
      uni.showActionSheet({
        itemList: res.suggestions.slice(0, 3),
        success: (r) => {
          content.value = res.suggestions[r.tapIndex] + '\n' + content.value
        }
      })
    } else if (res?.summary) {
      content.value = res.summary
      uni.showToast({ title: '已更新内容', icon: 'success' })
    } else {
      uni.showToast({ title: 'AI没有生成结果', icon: 'none' })
    }
  } catch (err) {
    console.error(err)
    // Error handling is done inside askAI or propagated. 
    // Since we removed the automated toast in api/ai.js, check detailed error here?
    // Actually api/ai.js throws, so we catch it here.
    let msg = 'AI暂不可用'
    if (err.statusCode === 429) msg = '请求太频繁，请稍后再试'
    else if (err.data && err.data.detail) msg = err.data.detail
    uni.showToast({ title: msg, icon: 'none' })
  } finally {
    aiLoading.value = false
    uni.hideLoading()
  }
}

const openMagicCompose = () => {
  if (aiLoading.value) return
  showAiSheet.value = true
}

const onAiAction = (index) => {
  if (index === 0) handleMagicResult('polish')
  if (index === 1) handleMagicResult('emojify')
  if (index === 2) handleMagicResult('title')
}

const uploadSingle = (filePath) =>
  new Promise((resolve, reject) => {
    const token = uni.getStorageSync('token') || ''
    uni.uploadFile({
      url: `${BASE_URL}/upload`,
      filePath,
      name: 'file',
      header: token ? { Authorization: `Bearer ${token}` } : {},
      success: (res) => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          try {
            const data = JSON.parse(res.data)
            resolve(data.url)
          } catch (e) {
            reject(e)
          }
        } else {
          let errMsg = 'Upload failed'
          try {
             const errData = JSON.parse(res.data)
             errMsg = errData.detail || errData.message || errMsg
          } catch (_) {
             errMsg = `Error ${res.statusCode}`
          }
          reject(new Error(errMsg))
        }
      },
      fail: (err) => {
        reject(new Error(err.errMsg || 'Network Error'))
      },
    })
  })

const submitPost = async () => {
  if (submitting.value) return
  if (!content.value.trim() && images.value.length === 0 && !video.value) {
    uni.showToast({ title: '请填写内容或选择媒体', icon: 'none' })
    return
  }

  submitting.value = true
  try {
    let mediaType = 'text'
    const uploaded = []

    // 1. Upload Images
    if (images.value.length > 0) {
      mediaType = 'image'
      for (const img of images.value) {
        const url = await uploadSingle(img)
        uploaded.push(url)
      }
    }
    // 2. Upload Video
    else if (video.value) {
      mediaType = 'video'
      const url = await uploadSingle(video.value)
      uploaded.push(url)
    }

    await post('/posts', {
      content: content.value,
      media_type: mediaType,
      media_urls: uploaded,
      tags: tags.value,
    })

    uni.showToast({ title: '发布成功', icon: 'success' })
    setTimeout(() => {
      uni.switchTab({ url: '/pages/index/index' })
    }, 400)
  } catch (err) {
    console.error(err)
    const msg = err.message || '发布失败'
    uni.showToast({ title: msg, icon: 'none' })
  } finally {
    submitting.value = false
  }
}
</script>

<style scoped>
.page {
  min-height: 100vh;
  background-color: var(--c-bg);
  background-image: radial-gradient(#dcdcdc 1px, transparent 1px);
  background-size: 20px 20px;
  padding: 30rpx;
  display: flex;
  flex-direction: column;
  gap: 40rpx;
}

/* --- Input Section --- */
.input-section {
  background: var(--c-white);
  border: var(--border-thick);
  border-radius: var(--radius-m);
  padding: 24rpx;
  box-shadow: var(--shadow-hard);
  display: flex;
  flex-direction: column;
  min-height: 380rpx;
  position: relative;
}

.main-input {
  flex: 1;
  width: 100%;
  min-height: 240rpx;
  font-size: 32rpx;
  line-height: 1.6;
  color: #111;
}

.tools-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 24rpx;
  padding-top: 16rpx;
  border-top: 4rpx dashed #eee;
}

.word-count {
  font-size: 24rpx;
  color: #9ca3af;
  font-weight: 700;
}
.word-count.warning { color: var(--c-purple); }

.ai-btn {
  background: var(--c-yellow);
  padding: 10rpx 24rpx;
  border: var(--border-thick);
  border-radius: var(--radius-full);
  font-size: 26rpx;
  font-weight: 800;
  box-shadow: 2rpx 2rpx 0px 0px #000;
}
.ai-btn:active {
  transform: translate(2rpx, 2rpx);
  box-shadow: none;
}

/* --- Tags Section --- */
.tags-section {
  background: var(--c-white);
  border: var(--border-thick);
  border-radius: var(--radius-m);
  padding: 24rpx;
  box-shadow: var(--shadow-hard);
  display: flex;
  flex-direction: column;
  gap: 20rpx;
}

.section-title-sm {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 28rpx;
  font-weight: 800;
  margin-bottom: 8rpx;
}

.input-row {
  display: flex;
  align-items: center;
  gap: 12rpx;
  border-bottom: 2rpx solid #eee;
  padding-bottom: 12rpx;
}

.hash-icon {
  font-size: 32rpx;
  font-weight: 900;
  color: var(--c-blue);
}

.tag-input {
  flex: 1;
  font-size: 28rpx;
  height: 60rpx;
}

.add-btn-mini {
  width: 50rpx;
  height: 50rpx;
  background: var(--c-black);
  color: #fff;
  border-radius: 50%;
  text-align: center;
  line-height: 46rpx;
  font-size: 32rpx;
  font-weight: 300;
}

.tags-list {
  display: flex;
  flex-wrap: wrap;
  gap: 16rpx;
}

.tag-pill {
  display: inline-flex;
  align-items: center;
  gap: 8rpx;
  padding: 8rpx 20rpx;
  background: #E0F2FE;
  border: 2rpx solid #000;
  border-radius: 999px;
  font-size: 24rpx;
  font-weight: 700;
  box-shadow: 2rpx 2rpx 0px 0px #000;
}
.tag-pill .close {
  font-size: 28rpx;
  color: #666;
  margin-left: 4rpx;
}

/* --- Media Section --- */
.media-section {
  display: flex;
  flex-direction: column;
  gap: 20rpx;
}

.section-title {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 30rpx;
  font-weight: 900;
  margin-left: 8rpx;
}

.limit-hint {
  font-size: 24rpx;
  color: #6b7280;
  font-weight: 400;
}

.picker-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20rpx;
}

.img-box {
  position: relative;
  width: 100%;
  padding-top: 100%;
  border-radius: var(--radius-m);
  overflow: hidden;
  background: #fff;
}
/* neu-card-sm style specific to images */
.neu-card-sm {
  border: var(--border-thick);
  box-shadow: 4rpx 4rpx 0px 0px #000;
}

.img-box image,
.preview-video {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.remove-btn {
  position: absolute;
  top: 8rpx;
  right: 8rpx;
  background: rgba(0,0,0,0.7);
  color: #fff;
  width: 40rpx;
  height: 40rpx;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20rpx;
  z-index: 10;
}

.add-box {
  position: relative;
  width: 100%;
  padding-top: 100%;
  border-radius: var(--radius-m);
  border: 4rpx dashed #000;
  background: rgba(255,255,255,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}
.add-box:active {
  background: rgba(0,0,0,0.05);
  border-style: solid;
}
.add-box .plus-icon {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 60rpx;
  color: #000;
  font-weight: 300;
}

/* --- Footer Action --- */
.footer-action {
  margin-top: auto; /* Push to bottom */
  padding-bottom: 20rpx;
}

.neu-btn-lg {
  width: 100%;
  height: 100rpx;
  line-height: 100rpx;
  background: var(--c-cyan);
  border: var(--border-thick);
  border-radius: var(--radius-m);
  font-size: 36rpx;
  font-weight: 900;
  box-shadow: var(--shadow-hard);
  color: #000;
}
.neu-btn-lg:active {
  transform: translate(4rpx, 4rpx);
  box-shadow: none;
}
</style>
