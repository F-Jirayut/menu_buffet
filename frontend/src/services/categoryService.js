import { axiosInstance } from '@/services/axiosConfig'

const prefix = 'menu_categories'

export const getMenuCategories = async () => {
    return await axiosInstance.get(`/${prefix}`)
}

export const createMenuCategory = async (data) => {
    return await axiosInstance.post(`/${prefix}`, data)
}

export const updateMenuCategory = async (id, data) => {
    return await axiosInstance.put(`/${prefix}/${id}`, data)
}

export const deleteMenuCategory = async (id) => {
    return await axiosInstance.delete(`/${prefix}/${id}`)
}

export const getMenuCategoryById = async (id) => {
    return await axiosInstance.get(`/${prefix}/${id}`)
}
