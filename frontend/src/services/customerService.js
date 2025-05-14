import { axiosInstance } from '@/services/axiosConfig'

const prefix = 'customers'

export const getCustomers = async ({ page = 1, page_size = 10, search = null }) => {
    return await axiosInstance.get(`/${prefix}`, {
        params: { page, page_size, search },
    })
}

export const createCustomer = async (data) => {
    return await axiosInstance.post(`/${prefix}`, data)
}

export const updateCustomer = async (id, data) => {
    return await axiosInstance.put(`/${prefix}/${id}`, data)
}

export const deleteCustomer = async (id) => {
    return await axiosInstance.delete(`/${prefix}/${id}`)
}

export const getCustomerById = (id, params = {}) => {
    return axiosInstance.get(`/${prefix}/${id}`, params)
}
