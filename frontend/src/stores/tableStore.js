import { defineStore } from 'pinia';
import { createGenericStore } from './genericFactoryStore';
import * as tableService from '@/services/tableService';

export const useTableStore = defineStore('table', () => {
  return createGenericStore({
    getAll: tableService.getTables,
    getById: tableService.getTableById,
    create: tableService.createTable,
    update: tableService.updateTable,
    delete: tableService.deleteTable,
  });
});
