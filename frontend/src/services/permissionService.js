import { axiosInstance } from '@/services/axiosConfig'

const prefix = 'permissions'

export const getPermissions = async ({ page = 1, page_size = 10, search = null }) => {
    return await axiosInstance.get(`/permissions`, {
      params: { page, page_size, search },
    })
  }

export const createPermission = async (data) => {
    return await axiosInstance.post(`/${prefix}`, data)
}

export const updatePermission = async (id, data) => {
    return await axiosInstance.put(`/${prefix}/${id}`, data)
}

export const deletePermission = async (id) => {
    return await axiosInstance.delete(`/${prefix}/${id}`)
}

export const getPermissionById = async (id) => {
    return await axiosInstance.get(`/${prefix}/${id}`)
}

export const getPermissionGroups = async () => {
    return await axiosInstance.get(`/${prefix}/groups/list`)
}