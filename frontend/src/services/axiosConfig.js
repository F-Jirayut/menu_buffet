import axios from 'axios'

const API = import.meta.env.VITE_API_BASE_URL

const axiosInstance = axios.create({
  baseURL: API,
})

const setAuthorizationHeader = (token) => {
  if (token) {
    axiosInstance.defaults.headers['Authorization'] = `Bearer ${token}`
  } else {
    delete axiosInstance.defaults.headers['Authorization']
  }
}

const loadTokenFromStorage = () => {
  const token = localStorage.getItem('access_token')
  setAuthorizationHeader(token)
}

axiosInstance.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

export { axiosInstance, setAuthorizationHeader, loadTokenFromStorage }
