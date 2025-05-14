import { authMiddleware } from '@/middleware/authMiddleware'
import CustomersView from "@/views/admin/customers/CustomersView.vue";
import CustomerEditView from '@/views/admin/customers/CustomerEditView.vue';

export default [
    {
        path: '/admin/customers',
        name: 'Customers',
        component: CustomersView,
        beforeEnter: authMiddleware,
        meta: {
            permissions: ['Customer.View'],
            breadcrumb:[{ name: 'ลูกค้า' }]
            
        }
    },
    {
        path: '/admin/customers/edit/:id?',
        name: 'CustomerEdit',
        component: CustomerEditView,
        beforeEnter: authMiddleware,
        meta: {
            permissions: {
                create: 'Customer.Create',
                update: 'Customer.Update'
            },
            breadcrumb: (route) => {
                return [
                  { name: 'ลูกค้า', to: '/admin/customers' },
                  { name: route.params.id ? 'ดู / แก้ไขลูกค้า' : 'เพิ่มลูกค้า' }
                ]
            },
        }
    },
]