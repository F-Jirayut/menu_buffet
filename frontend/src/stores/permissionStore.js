import { defineStore } from 'pinia';
import { ref } from 'vue';
import { getPermissions, createPermission, updatePermission, deletePermission, getPermissionGroups, getPermissionById } from '@/services/permissionService';

export const usePermissionStore = defineStore('permission', () => {
  const permissions = ref([]);
  const permissionGroups = ref([]);
  const loading = ref(false);
  const error = ref(null);

  const fetchDataById = async (id) => {
    loading.value = true;
    error.value = null;
    try {
      const response = await getPermissionById(id);
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
      const response = await getPermissions();
      const { success, message, data } = response.data;
      permissions.value = data;
      // console.log('Role Permissions:', permissions.value.role); // ['view', 'create', 'update', 'delete']
      // console.log('User Permissions:', permissions.value.user); // ['view', 'create', 'update', 'delete']
      // console.log('Permission Permissions:', permissions.value.permission); // ['view', 'create', 'update', 'delete']

      // for (const [key, values] of Object.entries(permissions.value)) {
      //   console.log(`${key} Permissions:`);
      //   values.forEach((perm, index) => {
      //     console.log(`  ${index + 1}. ${perm}`);
      //   });
      // }


    } catch (err) {
      error.value = err.response?.data?.detail || err.message || 'Failed to fetch data';
    } finally {
      loading.value = false;
    }
  };

  const fetchPermissionGroups = async () => {
    loading.value = true;
    error.value = null;
    try {
      const response = await getPermissionGroups();
      console.log(response)
      const { success, message, data } = response.data;
      permissionGroups.value = data;
      return data;
    } catch (err) {
      error.value = err.response?.data?.detail || err.message || 'Failed to fetch data';
    } finally {
      loading.value = false;
    }
  }

  const createData = async (permissionData) => {
    loading.value = true;
    error.value = null;
    try {
      const response = await createPermission(permissionData);
      const { success, message, data } = response.data;
      permissions.value.push(data);
    } catch (err) {
      error.value = err.response?.data?.detail || err.message || 'Failed to Create data';
    } finally {
      loading.value = false;
    }
  };

  const editData = async (id, updatedData) => {
    loading.value = true;
    error.value = null;
    try {
      const response = await updatePermission(id, updatedData);
      const index = permissions.value.findIndex(permission => permission.id === id);
      if (index !== -1) {
        permissions.value[index] = response.data;
      }
    } catch (err) {
      error.value = err.response?.data?.detail || err.message || 'Failed to Update data';
    } finally {
      loading.value = false;
    }
  };

  const deleteData = async (id) => {
    loading.value = true;
    error.value = null;
    try {
      await deletePermission(id);
      permissions.value = permissions.value.filter(permission => permission.id !== id);
    } catch (err) {
      error.value = err.response?.data?.detail || err.message || 'Failed to delete data';
    } finally {
      loading.value = false;
    }
  };
  return {
    permissions,
    permissionGroups,
    loading,
    error,
    fetchDataById,
    fetchData,
    fetchPermissionGroups,
    createData,
    editData,
    deleteData,
  };
});
