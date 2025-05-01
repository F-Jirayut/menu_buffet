import { authMiddleware } from '@/middleware/authMiddleware'
import TablesView from "@/views/admin/tables/TablesView.vue";
import TableEditView from '@/views/admin/tables/TableEditView.vue';

export default [
    {
        path: '/admin/tables',
        name: 'Tables',
        component: TablesView,
        beforeEnter: authMiddleware,
        meta: {
            permissions: ['Table.View'],
            breadcrumb: [{ name: 'โต๊ะ' }]
        }
    },
    {
        path: '/admin/tables/edit/:id?',
        name: 'TableEdit',
        component: TableEditView,
        beforeEnter: authMiddleware,
        meta: {
            permissions: {
                create: 'Table.Create',
                update: 'Table.Update'
            },
            breadcrumb: (route) => {
                return [
                  { name: 'โต๊ะ', to: '/admin/tables' },
                  { name: route.params.id ? 'ดู / แก้ไขโต๊ะ' : 'เพิ่มโต๊ะ' }
                ]
            },
        }
    },
]