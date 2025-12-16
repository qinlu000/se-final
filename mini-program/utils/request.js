export const BASE_URL = 'http://localhost:8000'

export function request({ url, method = 'GET', data = {}, header = {} }) {
  const token = uni.getStorageSync('token')
  const headers = { ...header }
  if (token) {
    headers.Authorization = `Bearer ${token}`
  }

  return new Promise((resolve, reject) => {
    uni.request({
      url: BASE_URL + url,
      method,
      data,
      header: headers,
      success: (res) => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve(res.data)
        } else if (res.statusCode === 401) {
          uni.removeStorageSync('token')
          uni.showToast({ title: '登录已过期', icon: 'none' })
          setTimeout(() => {
            uni.reLaunch({ url: '/pages/login/login' })
          }, 1500)
          reject(res)
        } else {
          reject(res)
        }
      },
      fail: reject,
    })
  })
}

export function get(url, params = {}) {
  return request({ url, method: 'GET', data: params })
}

export function post(url, data = {}) {
  return request({ url, method: 'POST', data })
}

export function del(url, data = {}) {
  return request({ url, method: 'DELETE', data })
}
