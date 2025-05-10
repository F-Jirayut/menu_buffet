import { defineStore } from 'pinia';
import { createGenericStore } from './genericFactoryStore';
import * as roleService from '@/services/roleService';

export const useRoleStore = defineStore('role', () => {
  return createGenericStore({
    getAll: roleService.getRoles,
    getById: roleService.getRoleById,
    create: roleService.createRole,
    update: roleService.updateRole,
    delete: roleService.deleteRole,
  });
});
