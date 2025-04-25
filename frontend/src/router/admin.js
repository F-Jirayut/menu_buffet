import DashboardView from "@/views/admin/DashboardView.vue";
import LoginView from "@/views/admin/LoginView.vue";
import { authMiddleware } from '@/middleware/authMiddleware'

export default [
    {
        path: '/admin/dashboard',
        name: 'Dashboard',
        component: DashboardView,
        beforeEnter: authMiddleware,
    },
    {
        path: '/admin/login',
        name: 'Login',
        component: LoginView,
        beforeEnter: authMiddleware,
    },
]