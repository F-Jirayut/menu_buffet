import { authMiddleware } from '@/middleware/authMiddleware'
import PermissionsView from "@/views/admin/permissions/PermissionsView.vue";
import PermissionEditView from "@/views/admin/permissions/PermissionEditView.vue";

export default [
    {
        path: '/admin/permissions',
        name: 'Permissions',
        component: PermissionsView,
        beforeEnter: authMiddleware,
        meta: {
            permissions: ['Permission.View'],
        }
    },
    {
        path: '/admin/permissions/edit/:id?',
        name: 'PermissionEdit',
        component: PermissionEditView,
        beforeEnter: authMiddleware,
        meta: {
            permissions: {
                create: 'Permission.Create',
                update: 'Permission.Update'
            }
        }
    },
]