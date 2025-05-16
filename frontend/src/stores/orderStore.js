import { defineStore } from 'pinia';
import { createGenericStore } from './genericFactoryStore';
import * as orderService from '@/services/orderService';
import { ref } from 'vue';

export const useOrderStore = defineStore('order', () => {
  const {
    items,
    orders,
    pagination,
    loading,
    error,
    fetchData,
    fetchDataById,
    createData,
    editData,
    deleteData
  } = createGenericStore({
    getAll: orderService.getOrders,
    getById: orderService.getOrderById,
    create: orderService.createOrder,
    update: orderService.updateOrder,
    delete: orderService.deleteOrder
  });

  const listStatus = ref(['pending', 'reserved', 'active', 'completed', 'cancelled']);

  return {
    items,
    orders,
    pagination,
    loading,
    error,
    fetchData,
    fetchDataById,
    createData,
    editData,
    deleteData,
    listStatus,
  };
});
