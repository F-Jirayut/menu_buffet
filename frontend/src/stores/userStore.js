import { defineStore } from 'pinia';
import { ref } from 'vue';
import { getUsers, createUser, updateUser, deleteUser, getUserById } from '@/services/userService';

export const useUserStore = defineStore('user', () => {
  const user = ref({});
  const users = ref([]);
  const loading = ref(false);
  const error = ref(null);

  const fetchDataById = async (id) => {
    loading.value = true;
    error.value = null;
    try {
      const response = await getUserById(id);
      const { success, message, data } = response.data;
      user.value = data;
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
      const response = await getUsers();
      const { success, message, data } = response.data;
      users.value = data;
    } catch (err) {
      error.value = err.response?.data?.detail || err.message || 'Failed to fetch data';
    } finally {
      loading.value = false;
    }
  };

  const createData = async (userData) => {
    loading.value = true;
    error.value = null;
    try {
      const response = await createUser(userData);
      const { success, message, data } = response.data;
      users.value.push(data);
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
      const response = await updateUser(id, updatedData);
      const index = users.value.findIndex(user => user.id === id);
      if (index !== -1) {
        users.value[index] = response.data;
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
      await deleteUser(id);
      users.value = users.value.filter(user => user.id !== id);
    } catch (err) {
      error.value = err.response?.data?.detail || err.message || 'Failed to delete data';
    } finally {
      loading.value = false;
    }
  };
  return {
    user,
    users,
    loading,
    error,
    fetchDataById,
    fetchData,
    createData,
    editData,
    deleteData,
  };
});
