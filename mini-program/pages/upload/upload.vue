<template>
  <view class="page">
    <view class="top-bar">
      <text class="title">发布</text>
      <button class="post-btn" :disabled="submitting" @click="submitPost">发布</button>
    </view>

    <view class="form">
      <textarea
        v-model="content"
        class="text-area"
        placeholder="这一刻的想法..."
        :maxlength="500"
        auto-height
      />

      <view class="picker">
        <view class="picker-grid">
          <view v-for="(img, idx) in images" :key="idx" class="img-box">
            <image :src="img" mode="aspectFill" />
            <view class="remove" @click="removeImage(idx)">✕</view>
          </view>
          <view v-if="images.length < 9" class="add-box" @click="chooseImages">
            <text>＋</text>
            <text class="hint">图片</text>
          </view>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref } from 'vue'
import { post, BASE_URL } from '../../utils/request'

const content = ref('')
const images = ref([])
const submitting = ref(false)

const chooseImages = () => {
  uni.chooseImage({
    count: 9 - images.value.length,
    sizeType: ['compressed'],
    success: (res) => {
      images.value = images.value.concat(res.tempFilePaths)
    },
  })
}

const removeImage = (idx) => {
  images.value.splice(idx, 1)
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
          reject(res)
        }
      },
      fail: reject,
    })
  })

const submitPost = async () => {
  if (submitting.value) return
  if (!content.value.trim() && images.value.length === 0) {
    uni.showToast({ title: '请填写内容或选择图片', icon: 'none' })
    return
  }

  submitting.value = true
  try {
    const uploaded = []
    for (const img of images.value) {
      const url = await uploadSingle(img)
      uploaded.push(url)
    }

    const mediaType = uploaded.length > 0 ? 'image' : 'text'
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
    uni.showToast({ title: '发布失败', icon: 'none' })
  } finally {
    submitting.value = false
  }
}
</script>

<style scoped>
.page {
  min-height: 100vh;
  background: #ededed;
  padding-bottom: 40rpx;
}

.top-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 24rpx 32rpx;
  background: #ffffff;
}

.title {
  font-weight: 700;
  color: #1f2937;
}

.post-btn {
  background: #07c160;
  color: #ffffff;
  border: none;
  border-radius: 30rpx;
  padding: 0 32rpx;
  height: 60rpx;
  line-height: 60rpx;
}

.form {
  margin: 16rpx;
  background: #ffffff;
  border-radius: 16rpx;
  padding: 20rpx;
}

.text-area {
  width: 100%;
  min-height: 200rpx;
  font-size: 30rpx;
  line-height: 1.5;
}

.picker {
  margin-top: 16rpx;
}

.picker-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12rpx;
}

.img-box {
  position: relative;
  width: 100%;
  padding-top: 100%;
  border-radius: 12rpx;
  overflow: hidden;
  background: #f3f4f6;
}

.img-box image {
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
  width: 36rpx;
  height: 36rpx;
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.55);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24rpx;
}

.add-box {
  width: 100%;
  padding-top: 100%;
  border-radius: 12rpx;
  border: 2rpx dashed #cbd5e1;
  color: #6b7280;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  gap: 8rpx;
}

.add-box text {
  font-size: 40rpx;
}

.hint {
  font-size: 24rpx;
}
</style>
