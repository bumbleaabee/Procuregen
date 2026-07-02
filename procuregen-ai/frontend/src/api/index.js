import axios from 'axios'
import { ElMessage } from 'element-plus'

const api = axios.create({
  baseURL: '/api',
  timeout: 30000,
})

// 响应拦截器
api.interceptors.response.use(
  (res) => {
    if (res.data && res.data.success === false) {
      ElMessage.error(res.data.message || '请求失败')
    }
    return res.data
  },
  (err) => {
    ElMessage.error(err.message || '网络错误')
    return Promise.reject(err)
  }
)

export default api
