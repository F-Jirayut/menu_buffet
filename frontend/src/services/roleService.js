import { axiosInstance } from '@/services/axiosConfig'

export const getRoles = async () => {
    return await axiosInstance.get('/roles')
}

export const createRole = async (data) => {
    return await axiosInstance.post('/roles', data)
}

export const updateRole = async (id, data) => {
    return await axiosInstance.put(`/roles/${id}`, data)
}

export const deleteRole = async (id) => {
    return await axiosInstance.delete(`/roles/${id}`)
}

export const getRoleById = (id, params = {}) => {
    return axiosInstance.get(`/roles/${id}`, params)
}
