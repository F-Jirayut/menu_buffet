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
            breadcrumb: [{ name: 'สิทธิ์การใช้งาน' }]
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
            },
            breadcrumb: (route) => {
                return [
                  { name: 'สิทธิ์การใช้งาน', to: '/admin/permissions' },
                  { name: route.params.id ? 'รายละเอียดสิทธิ์การใช้งาน' : 'เพิ่มสิทธิ์การใช้งาน' }
                ]
            },
        }
    },
]