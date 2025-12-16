<template>
  <view class="page">
    <view class="top-bar neu-card">
      <text class="title">发布</text>
    </view>

    <view class="form neu-card">
      <textarea
        v-model="content"
        class="text-area"
        placeholder="这一刻的想法..."
        :maxlength="500"
        auto-height
      />
      <view class="ai-row">
        <button class="neu-btn ai-btn" @click="openMagicCompose">🪄 AI 帮写</button>
      </view>

      <view class="picker">
        <view class="picker-grid">
          <view v-for="(img, idx) in images" :key="idx" class="img-box">
            <image :src="img" mode="aspectFill" />
            <view class="remove" @click="removeImage(idx)">✕</view>
          </view>
          
          <view v-if="video" class="img-box">
             <video :src="video" class="preview-video" :controls="false" :show-center-play-btn="false"></video>
             <view class="remove" @click="removeVideo">✕</view>
          </view>

          <view v-if="images.length < 9 && !video" class="add-box" @click="chooseImages">
            <text>＋</text>
            <text class="hint">媒体</text>
          </view>
        </view>
      </view>
    </view>

    <button class="post-btn neu-btn full-btn" :disabled="submitting" @click="submitPost">发布</button>
  
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
const submitting = ref(false)
const aiLoading = ref(false)
const showAiSheet = ref(false)
const aiActions = ['🪄 润色内容', '😀 添加 Emoji', '🏷️ 生成标题']

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
    uni.showToast({ title: 'AI暂不可用', icon: 'none' })
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
      tags: [],
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
  background-size: 18px 18px;
  padding: 24rpx 24rpx 60rpx;
  display: flex;
  flex-direction: column;
  gap: 20rpx;
}

.top-bar {
  padding: 22rpx 26rpx;
  display: flex;
  align-items: center;
  justify-content: flex-start;
  border: var(--border-thick);
  box-shadow: var(--shadow-hard);
}

.title {
  font-weight: 900;
  font-size: 34rpx;
  letter-spacing: 0.6rpx;
}

.form {
  background: var(--c-white);
  border-radius: var(--radius-m);
  padding: 24rpx;
  border: var(--border-thick);
  box-shadow: var(--shadow-hard);
  display: flex;
  flex-direction: column;
  gap: 18rpx;
}

.text-area {
  width: 100%;
  min-height: 200rpx;
  font-size: 30rpx;
  line-height: 1.5;
  border: var(--border-thick);
  border-radius: var(--radius-m);
  background: var(--c-white);
  padding: 18rpx;
  box-shadow: var(--shadow-hard);
}

.ai-row {
  display: flex;
  justify-content: flex-end;
}

.ai-btn {
  padding: 14rpx 26rpx;
  font-size: 28rpx;
  font-weight: 900;
  background-color: var(--c-yellow);
  border: var(--border-thick);
  box-shadow: var(--shadow-hard);
  display: flex;
  align-items: center;
  gap: 8rpx;
}

.ai-btn:active {
  transform: translate(2rpx, 2rpx);
  box-shadow: none;
}

.picker {
  margin-top: 10rpx;
}

.picker-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16rpx;
}

.img-box {
  position: relative;
  width: 100%;
  padding-top: 100%;
  border-radius: var(--radius-m);
  overflow: hidden;
  background: var(--c-white);
  border: var(--border-thick);
  box-shadow: var(--shadow-hard);
}

.img-box image,
.preview-video {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.remove {
  position: absolute;
  top: 8rpx;
  right: 8rpx;
  width: 40rpx;
  height: 40rpx;
  border-radius: 50%;
  background: var(--c-black);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24rpx;
  border: var(--border-thin);
}

.add-box {
  width: 100%;
  padding-top: 100%;
  border-radius: var(--radius-m);
  border: var(--border-thick);
  color: var(--c-black);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  gap: 8rpx;
  background: var(--c-white);
  box-shadow: var(--shadow-hard);
  transition: background 0.1s ease;
}

.add-box:active {
  background: var(--c-yellow);
}

.add-box text {
  font-size: 44rpx;
  font-weight: 900;
}

.hint {
  font-size: 24rpx;
  font-weight: 700;
}

.post-btn {
  width: 100%;
  height: 88rpx;
  line-height: 88rpx;
  font-size: 32rpx;
  border-radius: var(--radius-m);
  box-shadow: var(--shadow-hard);
}

.post-btn:disabled {
  opacity: 0.6;
}

.full-btn {
  margin-top: 4rpx;
}
</style>
