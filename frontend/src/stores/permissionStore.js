import { defineStore } from 'pinia';
import { createGenericStore } from './genericFactoryStore';
import * as permissionService from '@/services/permissionService';
import { ref } from 'vue';

export const usePermissionStore = defineStore('permission', () => {
  const {
    items,
    permissions,
    pagination,
    loading,
    error,
    fetchData,
    fetchDataById,
    createData,
    editData,
    deleteData
  } = createGenericStore({
    getAll: permissionService.getPermissions,
    getById: permissionService.getPermissionById,
    create: permissionService.createPermission,
    update: permissionService.updatePermission,
    delete: permissionService.deletePermission
  });

  const permissionGroups = ref([]);

  const fetchPermissionGroups = async () => {
    loading.value = true;
    error.value = null;
    try {
      const response = await permissionService.getPermissionGroups();
      permissionGroups.value = response.data.data;
    } catch (err) {
      error.value = err.response?.data?.detail || err.message || 'Failed to fetch permission groups';
    } finally {
      loading.value = false;
    }
  };

  return {
    items,
    permissions,
    pagination,
    loading,
    error,
    fetchData,
    fetchDataById,
    createData,
    editData,
    deleteData,
    fetchPermissionGroups,
    permissionGroups
  };
});
