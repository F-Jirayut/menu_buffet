import { ref } from 'vue';

export function createGenericStore(service) {
  const items = ref([]);
  const pagination = ref({});
  const loading = ref(false);
  const error = ref(null);

  const fetchData = async (params = {}) => {
    loading.value = true;
    error.value = null;
    try {
      const response = await service.getAll(params);
      console.log(response)
      items.value = response.data.data;
      pagination.value = response.data.pagination || {};
    } catch (err) {
      error.value = err.response?.data?.detail || err.message || 'Failed to fetch data';
    } finally {
      loading.value = false;
    }
  };

  const fetchDataById = async (id, options = {}) => {
    loading.value = true;
    error.value = null;
    try {
      const response = await service.getById(id, options);
      return response.data.data;
    } catch (err) {
      error.value = err.response?.data?.detail || err.message || 'Failed to fetch data';
    } finally {
      loading.value = false;
    }
  };

  const createData = async (data) => {
    loading.value = true;
    error.value = null;
    try {
      const response = await service.create(data);
      items.value.push(response.data.data);
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
      const response = await service.update(id, updatedData);
      const index = items.value.findIndex(item => item.id === id);
      if (index !== -1) {
        items.value[index] = response.data.data;
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
      await service.delete(id);
      items.value = items.value.filter(item => item.id !== id);
    } catch (err) {
      error.value = err.response?.data?.detail || err.message || 'Failed to delete data';
    } finally {
      loading.value = false;
    }
  };

  return {
    items,
    pagination,
    loading,
    error,
    fetchData,
    fetchDataById,
    createData,
    editData,
    deleteData,
  };
}
