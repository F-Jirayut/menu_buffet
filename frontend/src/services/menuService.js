import { axiosInstance } from '@/services/axiosConfig'

const prefix = 'menus'

export const getMenus = async ({ page = 1, page_size = 10, search = null }) => {
    return await axiosInstance.get(`/${prefix}`, {
        params: { page, page_size, search },
    })
}

export const createMenu = async (data) => {
    return await axiosInstance.post(`/${prefix}`, data)
}

export const updateMenu = async (id, data) => {
    return await axiosInstance.put(`/${prefix}/${id}`, data)
}

export const deleteMenu = async (id) => {
    return await axiosInstance.delete(`/${prefix}/${id}`)
}

export const getMenuById = async (id) => {
    return await axiosInstance.get(`/${prefix}/${id}`)
}
