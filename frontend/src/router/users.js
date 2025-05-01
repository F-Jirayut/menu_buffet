import UsersView from "@/views/admin/users/UsersView.vue";
import UserEditView from "@/views/admin/users/UserEditView.vue";
import { authMiddleware } from '@/middleware/authMiddleware'

export default [
    {
        path: '/admin/users',
        name: 'Users',
        component: UsersView,
        beforeEnter: authMiddleware,
        meta: {
            permissions: ['User.View'],
            breadcrumb: [{ name: 'ผู้ใช้งาน' }],
          }
    },
    {
        path: '/admin/users/edit/:id?',
        name: 'UserEdit',
        component: UserEditView,
        beforeEnter: authMiddleware,
        meta: {
            permissions: {
                create: 'User.Create',
                update: 'User.Update'
            },
            breadcrumb: (route) => {
                return [
                  { name: 'ผู้ใช้งาน', to: '/admin/users' },
                  { name: route.params.id ? 'ดู / แก้ไขผู้ใช้งาน' : 'เพิ่มผู้ใช้งาน' }
                ]
            },
        }
    }
]