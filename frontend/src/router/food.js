import { authMiddleware } from '@/middleware/authMiddleware'
import MenuEdit from '@/views/admin/foods/menu/MenuEdit.vue'
import MenuView from '@/views/admin/foods/menu/MenuView.vue'
import CategoriesView from '@/views/admin/foods/categories/CategoriesView.vue'
import CategoryEdit from '@/views/admin/foods/categories/CategoryEdit.vue'

export default [
    {
        path: '/admin/foods/menus',
        name: 'Menus',
        component: MenuView,
        beforeEnter: authMiddleware,
        meta : {
            permissions: ['Menu.View'],
            breadcrumb:  [{ name: 'เมนู' }]
        }
    },
    {
        path: '/admin/foods/menus/edit/:id?',
        name: 'MenuEdit',
        component: MenuEdit,
        beforeEnter: authMiddleware,
        meta : {
            permissions: {
                create: 'Menu.Create',
                update: 'Menu.Update'
            },
            breadcrumb: (route) => {
                return [
                  { name: 'เมนู', to: '/admin/foods/menus' },
                  { name: route.params.id ? 'ดู / แก้ไขเมนู' : 'เพิ่มเมนู' }
                ]
            },
        }
    },
    {
        path: '/admin/foods/categories',
        name: 'Categories',
        component: CategoriesView,
        beforeEnter: authMiddleware,
        meta : {
            permissions: ['Category.View'],
            breadcrumb:  [{ name: 'ประเภท' }]
        }
    },
    {
        path: '/admin/foods/categories/edit/:id?',
        name: 'CategoryEdit',
        component: CategoryEdit,
        beforeEnter: authMiddleware,
        meta : {
            permissions: {
                create: 'Category.Create',
                update: 'Category.Update'
            },
            breadcrumb: (route) => {
                return [
                  { name: 'ประเภท', to: '/admin/foods/categories' },
                  { name: route.params.id ? 'ดู / แก้ไขประเภท' : 'เพิ่มประเภท' }
                ]
            },
        }
    }
]