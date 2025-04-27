import { defineStore } from 'pinia';
import { ref } from 'vue';
import { getMenus, createMenu, updateMenu, deleteMenu, getMenuById } from '@/services/menuService';

export const useMenuStore = defineStore('menu', () => {
  const menu = ref({});
  const menus = ref([]);
  const pagination = ref({})
  const loading = ref(false);
  const error = ref(null);

  const fetchDataById = async (id) => {
    loading.value = true;
    error.value = null;
    try {
      const response = await getMenuById(id);
      const { success, message, data } = response.data;
      menu.value = data;
      return data;
    } catch (err) {
      error.value = err.response?.data?.detail || err.message || 'Failed to fetch data';
    } finally {
      loading.value = false;
    }
  }

  const fetchData = async (page = 1, pageSize = 10, search = null) => {
    loading.value = true;
    error.value = null;
    try {
      const response = await getMenus({ page, page_size: pageSize, search: search });
      const { success, message, data, pagination : paginationData } = response.data;
      menus.value = data;
      pagination.value = paginationData
    } catch (err) {
      error.value = err.response?.data?.detail || err.message || 'Failed to fetch data';
    } finally {
      loading.value = false;
    }
  };

  const createData = async (menuData) => {
    loading.value = true;
    error.value = null;
    try {
      const response = await createMenu(menuData);
      const { success, message, data } = response.data;
      menus.value.push(data);
    } catch (err) {
      error.value = err.response?.data?.detail || err.message || 'Failed to create data';
    } finally {
      loading.value = false;
    }
  };

  const editData = async (id, updatedData) => {
    loading.value = true;
    error.value = null;
    try {
      const response = await updateMenu(id, updatedData);
      const index = menus.value.findIndex(menu => menu.id === id);
      if (index !== -1) {
        menus.value[index] = response.data;
      }
    } catch (err) {
      error.value = err.response?.data?.detail || err.message || 'Failed to update data';
    } finally {
      loading.value = false;
    }
  };

  const deleteData = async (id) => {
    loading.value = true;
    error.value = null;
    try {
      await deleteMenu(id);
      menus.value = menus.value.filter(menu => menu.id !== id);
    } catch (err) {
      error.value = err.response?.data?.detail || err.message || 'Failed to delete data';
    } finally {
      loading.value = false;
    }
  };
  return {
    menu,
    menus,
    pagination,
    loading,
    error,
    fetchDataById,
    fetchData,
    createData,
    editData,
    deleteData,
  };
});
