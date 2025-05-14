import { authMiddleware } from '@/middleware/authMiddleware'
import OrdersView from "@/views/admin/orders/OrdersView.vue";
import OrderEditView from '@/views/admin/orders/OrderEditView.vue';

export default [
    {
        path: '/admin/orders',
        name: 'Orders',
        component: OrdersView,
        beforeEnter: authMiddleware,
        meta: {
            permissions: ['Order.View'],
            breadcrumb:[{ name: 'คำสั่งซื้อ' }]
            
        }
    },
    {
        path: '/admin/orders/edit/:id?',
        name: 'OrderEdit',
        component: OrderEditView,
        beforeEnter: authMiddleware,
        meta: {
            permissions: {
                create: 'Order.Create',
                update: 'Order.Update'
            },
            breadcrumb: (route) => {
                return [
                  { name: 'คำสั่งซื้อ', to: '/admin/orders' },
                  { name: route.params.id ? 'ดู / แก้ไขคำสั่งซื้อ' : 'เพิ่มคำสั่งซื้อ' }
                ]
            },
        }
    },
]