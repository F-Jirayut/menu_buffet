import { authMiddleware } from '@/middleware/authMiddleware'
import OrderItemEditView from '@/views/admin/orders/OrderItemEditView.vue';

export default [
    {
        path: '/admin/order-items/edit/:id?',
        name: 'OrderItemEdit',
        component: OrderItemEditView,
        beforeEnter: authMiddleware,
        meta: {
            permissions: {
                create: 'OrderItem.Create',
                update: 'OrderItem.Update'
            },
            breadcrumb: (route) => {
                return [
                  { name: 'คำสั่งซื้อ', to: '/admin/orders' },
                  { name: route.params.id ? 'รายละเอียดรายการอาหาร' : 'เพิ่มรายการอาหาร' }
                ]
            },
        }
    },
]