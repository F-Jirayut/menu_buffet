import { defineStore } from 'pinia';
import { createGenericStore } from './genericFactoryStore';
import * as orderService from '@/services/orderService';

export const useOrderStore = defineStore('order', () => {
  return createGenericStore({
    getAll: orderService.getOrders,
    getById: orderService.getOrderById,
    create: orderService.createOrder,
    update: orderService.updateOrder,
    delete: orderService.deleteOrder,
  });
});
