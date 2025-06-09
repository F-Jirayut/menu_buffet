import { defineStore } from 'pinia';
import { createGenericStore } from './genericFactoryStore';
import * as orderItemService from '@/services/orderItemService';
import { ref } from 'vue';

export const useOrderItemStore = defineStore('orderItem', () => {
  const {
    items,
    pagination,
    loading,
    error,
    fetchData,
    fetchDataById,
    createData,
    editData,
    deleteData
  } = createGenericStore({
    getAll: orderItemService.getOrderItems,
    getById: orderItemService.getOrderItemById,
    create: orderItemService.createOrderItem,
    update: orderItemService.updateOrderItems,
  });

  const listStatus = ref(["pending", "preparing", "served", "cancelled",]);
  const groupedItems = ref([]);

  const fetchDataGrouped = async (params = {}) => {
    loading.value = true;
    error.value = null;
    try {
      const response = await orderItemService.getOrderItemsGrouped(params);
      groupedItems.value = response.data.data;
    } catch (err) {
      error.value = err.response?.data?.detail || err.message || 'Failed to fetch grouped data';
    } finally {
      loading.value = false;
    }
  };

  return {
    items,
    groupedItems,
    pagination,
    loading,
    error,
    fetchData,
    fetchDataById,
    createData,
    editData,
    deleteData,
    listStatus,
    fetchDataGrouped,
  };
});
