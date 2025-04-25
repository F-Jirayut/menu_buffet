import { axiosInstance } from '@/services/axiosConfig'

export const login = async (username, password) => {
  return await axiosInstance.post('/auth/login', {
    username,
    password,
  })
}

export const getProfile = async () => {
  return await axiosInstance.get('/auth/profile')
}
