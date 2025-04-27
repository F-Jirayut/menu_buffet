import { axiosInstance } from '@/services/axiosConfig'

const prefix = 'options'

export const getOptions = async ({ type }) => {
    return await axiosInstance.get(`/${prefix}`, {
        params: { type },
    })
}
