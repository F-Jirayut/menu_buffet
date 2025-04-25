import { defineStore } from 'pinia';
import { ref } from 'vue';
import { getRoles, createRole, updateRole, deleteRole, getRoleById } from '@/services/roleService';

export const useRoleStore = defineStore('role', () => {
  const roles = ref([]);
  const loading = ref(false);
  const error = ref(null);

  const fetchDataById = async (id, options = {}) => {
    loading.value = true;
    error.value = null;
  
    try {
      // สมมุติว่า getRoleById รองรับการส่ง query เช่น ?include=permissions
      const response = await getRoleById(id, options);
      console.log('Role By ID:')
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
      const response = await getRoles();
      const { success, message, data } = response.data;
      roles.value = data;
    } catch (err) {
      error.value = err.response?.data?.detail || err.message || 'Failed to fetch data';
    } finally {
      loading.value = false;
    }
  };

  const createData = async (roleData) => {
    loading.value = true;
    error.value = null;
    try {
      const response = await createRole(roleData);
      const { success, message, data } = response.data;
      roles.value.push(data);
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
      const response = await updateRole(id, updatedData);
      const index = roles.value.findIndex(role => role.id === id);
      if (index !== -1) {
        roles.value[index] = response.data;
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
      await deleteRole(id);
      roles.value = roles.value.filter(role => role.id !== id);
    } catch (err) {
      error.value = err.response?.data?.detail || err.message || 'Failed to delete data';
    } finally {
      loading.value = false;
    }
  };
  return {
    roles,
    loading,
    error,
    fetchDataById,
    fetchData,
    createData,
    editData,
    deleteData,
  };
});
