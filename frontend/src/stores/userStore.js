import { defineStore } from 'pinia';
import { createGenericStore } from './genericFactoryStore';
import * as userService from '@/services/userService';

export const useUserStore = defineStore('user', () => {
  return createGenericStore({
    getAll: userService.getUsers,
    getById: userService.getUserById,
    create: userService.createUser,
    update: userService.updateUser,
    delete: userService.deleteUser,
  });
});
