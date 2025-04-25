import { authMiddleware } from '@/middleware/authMiddleware'
import RolesView from "@/views/admin/roles/RolesView.vue";
import RoleEditView from '@/views/admin/roles/RoleEditView.vue';

export default [
    {
        path: '/admin/roles',
        name: 'Roles',
        component: RolesView,
        beforeEnter: authMiddleware,
        meta: {
            permissions: ['Role.View'],
        }
    },
    {
        path: '/admin/roles/edit/:id?',
        name: 'RoleEdit',
        component: RoleEditView,
        beforeEnter: authMiddleware,
        meta: {
            permissions: {
                create: 'Role.Create',
                update: 'Role.Update'
            }
        }
    },
]