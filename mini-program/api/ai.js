import { request } from '../utils/request'

export const askAI = ({ content, mode = 'summary', tone = 'friendly', include_tags = true }) =>
  request({
    url: '/ai/assistant',
    method: 'POST',
    data: { content, mode, tone, include_tags }
  })
