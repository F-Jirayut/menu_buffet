import { axiosInstance } from '@/services/axiosConfig'

const prefix = 'order_items'

export const getOrderItems = async ({ page = 1, page_size = 10, search = null }) => {
    return await axiosInstance.get(`/${prefix}`, {
        params: { page, page_size, search },
    })
}

export const createOrderItem = async (data) => {
    return await axiosInstance.post(`/${prefix}`, data)
}

export const updateOrderItems = async (data) => {
    return await axiosInstance.put(`/${prefix}`, data)
}

export const deleteOrderItem = async (id) => {
    return await axiosInstance.delete(`/${prefix}/${id}`)
}

export const getOrderItemById = (id, params = {}) => {
    return axiosInstance.get(`/${prefix}/${id}`, params)
}
