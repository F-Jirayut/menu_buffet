import { axiosInstance } from '@/services/axiosConfig'

const prefix = 'roles'

export const getRoles = async ({ page = 1, page_size = 10, search = null }) => {
    return await axiosInstance.get(`/${prefix}`, {
        params: { page, page_size, search },
    })
}

export const createRole = async (data) => {
    return await axiosInstance.post(`/${prefix}`, data)
}

export const updateRole = async (id, data) => {
    return await axiosInstance.put(`/${prefix}/${id}`, data)
}

export const deleteRole = async (id) => {
    return await axiosInstance.delete(`/${prefix}/${id}`)
}

export const getRoleById = (id, params = {}) => {
    return axiosInstance.get(`/${prefix}/${id}`, params)
}
