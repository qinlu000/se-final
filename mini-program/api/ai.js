import { request } from '../utils/request'

export const askAI = async ({
  content,
  mode = 'summary',
  tone = 'friendly',
  include_tags = true,
  target_lang = 'zh'
} = {}) => {
  try {
    return await request({
      url: '/ai/assistant',
      method: 'POST',
      data: { content, mode, tone, include_tags, target_lang }
    })
  } catch (err) {
    console.error('AI request failed', err)
    uni.showToast({ title: 'AI服务暂不可用', icon: 'none' })
    throw err
  }
}
