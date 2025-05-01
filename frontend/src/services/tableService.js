import { axiosInstance } from '@/services/axiosConfig'

const prefix = 'tables'

export const getTables = async ({ search = null }) => {
    return await axiosInstance.get(`/${prefix}`, {
        params: { search },
    })
}

export const createTable = async (data) => {
    return await axiosInstance.post(`/${prefix}`, data)
}

export const updateTable = async (id, data) => {
    return await axiosInstance.put(`/${prefix}/${id}`, data)
}

export const deleteTable = async (id) => {
    return await axiosInstance.delete(`/${prefix}/${id}`)
}

export const getTableById = (id, params = {}) => {
    return axiosInstance.get(`/${prefix}/${id}`, params)
}
