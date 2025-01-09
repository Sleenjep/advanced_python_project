import { createRouter, createWebHistory} from "vue-router";
import LoginView from "@/views/LoginView.vue";
import RegistrationView from "@/views/RegistrationView.vue";
import ProductsView from "@/views/ProductsView.vue";
import ManageProductsView from "@/views/ManageProductsView.vue";
import ProfileView from "@/views/ProfileView.vue";
import CartView from "@/views/CartView.vue";
import ManageUsersView from "@/views/ManageUsersView.vue";
import DashboardView from "@/views/DashboardView.vue";

const routes = [
    {
        path: '/login',
        name: "Login",
        component: LoginView,
    },
    {
        path: '/registration',
        name: "Registration",
        component: RegistrationView,
    },
    {
        path: '/products',
        name: "Products",
        component: ProductsView
    },
    {
        path: '/manage_users',
        name: "ManageUsersView",
        component: ManageUsersView
    },
    {
        path: '/manage_products',
        name: "ManageProductsView",
        component: ManageProductsView
    },
    {
        path: '/dashboard',
        name: "DashboardView",
        component: DashboardView
    },
    {
        path: '/profile',
        name: "ProfileView",
        component: ProfileView
    },
    {
        path: '/cart',
        name: "CartView",
        component: CartView
    },
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

export default router