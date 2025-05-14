import { defineStore } from 'pinia';
import { createGenericStore } from './genericFactoryStore';
import * as menuService from '@/services/menuService';

export const useMenuStore = defineStore('menu', () => {
  return createGenericStore({
    getAll: menuService.getMenus,
    getById: menuService.getMenuById,
    create: menuService.createMenu,
    update: menuService.updateMenu,
    delete: menuService.deleteMenu,
  });
});
