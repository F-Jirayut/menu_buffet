import { axiosInstance } from '@/services/axiosConfig'

const prefix = 'order_items'

export const getOrderItems = async (
    { 
        date=new Date().toISOString().split('T')[0] ,
        // page = 1, 
        // page_size = 10, 
        // search = null, 
        order_by = ['created_at:desc'] 
    }) => {
    return await axiosInstance.get(`/${prefix}`, {
        params: { date, order_by },
        paramsSerializer: (params) => {
            const searchParams = new URLSearchParams()

            for (const key in params) {
                const value = params[key]
                if (Array.isArray(value)) {
                    value.forEach(v => searchParams.append(key, v))
                } else if (value !== null && value !== undefined) {
                    searchParams.append(key, value)
                }
            }

            return searchParams.toString()
        },
    })
}

export const getOrderItemsGrouped = async (
    { 
        date=new Date().toISOString().split('T')[0],
        status = null,
        order_by = ['created_at:desc'] 
    }) => {
    return await axiosInstance.get(`/${prefix}/grouped`, {
        params: { date, status, order_by },
        paramsSerializer: (params) => {
            const searchParams = new URLSearchParams()

            for (const key in params) {
                const value = params[key]
                if (Array.isArray(value)) {
                    value.forEach(v => searchParams.append(key, v))
                } else if (value !== null && value !== undefined) {
                    searchParams.append(key, value)
                }
            }

            return searchParams.toString()
        },
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
