import { axiosInstance } from '@/services/axiosConfig'

export const getUsers = async () => {
    return await axiosInstance.get('/users')
}

export const createUser = async (data) => {
    return await axiosInstance.post('/users', data)
}

export const updateUser = async (id, data) => {
    return await axiosInstance.put(`/users/${id}`, data)
}

export const deleteUser = async (id) => {
    return await axiosInstance.delete(`/users/${id}`)
}

export const getUserById = async (id) => {
    return await axiosInstance.get(`/users/${id}`)
}
