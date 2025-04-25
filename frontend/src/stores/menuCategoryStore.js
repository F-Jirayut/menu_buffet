import { defineStore } from 'pinia';
import { ref } from 'vue';
import { getMenuCategories, createMenuCategory, updateMenuCategory, deleteMenuCategory, getMenuCategoryById } from '@/services/categoryService';

export const useMenuCategoriestore = defineStore('menucategory', () => {
  const menuCategories = ref([]);
  const loading = ref(false);
  const error = ref(null);

  const fetchDataById = async (id) => {
    loading.value = true;
    error.value = null;
    try {
      const response = await getMenuCategoryById(id);
      const { success, message, data } = response.data;
      return data;
    } catch (err) {
      error.value = err.response?.data?.detail || err.message || 'Failed to fetch data';
    } finally {
      loading.value = false;
    }
  }

  const fetchData = async () => {
    loading.value = true;
    error.value = null;
    try {
      const response = await getMenuCategories();
      const { success, message, data } = response.data;
      menuCategories.value = data;

    } catch (err) {
      error.value = err.response?.data?.detail || err.message || 'Failed to fetch data';
    } finally {
      loading.value = false;
    }
  };

  const createData = async (menucategoryData) => {
    loading.value = true;
    error.value = null;
    try {
      const response = await createMenuCategory(menucategoryData);
      const { success, message, data } = response.data;
      menuCategories.value.push(data);
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
      const response = await updateMenuCategory(id, updatedData);
      const index = menuCategories.value.findIndex(menucategory => menucategory.id === id);
      if (index !== -1) {
        menuCategories.value[index] = response.data;
      }
    } catch (err) {
      console.log(err)
      error.value = err.response?.data?.detail || err.message || 'Failed to update data';
    } finally {
      loading.value = false;
    }
  };

  const deleteData = async (id) => {
    loading.value = true;
    error.value = null;
    try {
      await deleteMenuCategory(id);
      menuCategories.value = menuCategories.value.filter(menucategory => menucategory.id !== id);
    } catch (err) {
      error.value = err.response?.data?.detail || err.message || 'Failed to delete data';
    } finally {
      loading.value = false;
    }
  };
  return {
    menuCategories,
    loading,
    error,
    fetchDataById,
    fetchData,
    createData,
    editData,
    deleteData,
  };
});
