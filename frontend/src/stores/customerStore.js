import { defineStore } from 'pinia';
import { createGenericStore } from './genericFactoryStore';
import * as customerService from '@/services/customerService';

export const useCustomerStore = defineStore('customer', () => {
  return createGenericStore({
    getAll: customerService.getCustomers,
    getById: customerService.getCustomerById,
    create: customerService.createCustomer,
    update: customerService.updateCustomer,
    delete: customerService.deleteCustomer,
  });
});
