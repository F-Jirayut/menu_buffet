import { defineStore } from 'pinia';
import { createGenericStore } from './genericFactoryStore';
import * as menucategoryService from '@/services/categoryService';

export const useMenuCategoryStore = defineStore('menucategory', () => {
  return createGenericStore({
    getAll: menucategoryService.getMenuCategories,
    getById: menucategoryService.getMenuCategoryById,
    create: menucategoryService.createMenuCategory,
    update: menucategoryService.updateMenuCategory,
    delete: menucategoryService.deleteMenuCategory,
  });
});
