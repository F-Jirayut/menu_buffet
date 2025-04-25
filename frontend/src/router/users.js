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
            }
        }
    }
]