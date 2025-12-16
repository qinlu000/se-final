import { request } from '../utils/request'

export const askAI = async ({
  content,
  mode = 'summary',
  tone = 'friendly',
  include_tags = true,
  target_lang = 'zh'
} = {}) => {
  return await request({
    url: '/ai/assistant',
    method: 'POST',
    data: { content, mode, tone, include_tags, target_lang }
  })
}
