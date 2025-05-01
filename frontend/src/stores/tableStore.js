import { defineStore } from 'pinia';
import { ref } from 'vue';
import { getTables, createTable, updateTable, deleteTable, getTableById } from '@/services/tableService';

export const useTableStore = defineStore('table', () => {
  const tables = ref([]);
  const loading = ref(false);
  const error = ref(null);

  const fetchDataById = async (id, options = {}) => {
    loading.value = true;
    error.value = null;
  
    try {
      const response = await getTableById(id, options);
      const { success, message, data } = response.data;
      return data;
    } catch (err) {
      error.value = err.response?.data?.detail || err.message || 'Failed to fetch data';
    } finally {
      loading.value = false;
    }
  }
  

  const fetchData = async (search = null) => {
    loading.value = true;
    error.value = null;
    try {
      const response = await getTables({ search: search });
      const { success, message, data, } = response.data;
      tables.value = data;
    } catch (err) {
      error.value = err.response?.data?.detail || err.message || 'Failed to fetch data';
    } finally {
      loading.value = false;
    }
  };

  const createData = async (tableData) => {
    loading.value = true;
    error.value = null;
    try {
      const response = await createTable(tableData);
      const { success, message, data } = response.data;
      tables.value.push(data);
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
      const response = await updateTable(id, updatedData);
      const index = tables.value.findIndex(table => table.id === id);
      if (index !== -1) {
        tables.value[index] = response.data;
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
      await deleteTable(id);
      tables.value = tables.value.filter(table => table.id !== id);
    } catch (err) {
      error.value = err.response?.data?.detail || err.message || 'Failed to delete data';
    } finally {
      loading.value = false;
    }
  };
  return {
    tables,
    loading,
    error,
    fetchDataById,
    fetchData,
    createData,
    editData,
    deleteData,
  };
});
