import { axiosInstance } from '@/services/axiosConfig'

const prefix = 'orders'

export const getOrders = async ({ page = 1, page_size = 10, search = null }) => {
    return await axiosInstance.get(`/${prefix}`, {
        params: { page, page_size, search },
    })
}

export const createOrder = async (data) => {
    return await axiosInstance.post(`/${prefix}`, data)
}

export const updateOrder = async (id, data) => {
    return await axiosInstance.put(`/${prefix}/${id}`, data)
}

export const deleteOrder = async (id) => {
    return await axiosInstance.delete(`/${prefix}/${id}`)
}

export const getOrderById = (id, params = {}) => {
    return axiosInstance.get(`/${prefix}/${id}`, params)
}
