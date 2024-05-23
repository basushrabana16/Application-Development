import Vue from 'vue';
import Router from 'vue-router';
import HomePage from './components/Home.vue'
import LogIn from './components/Login.vue'
import RegisTer from './components/Register.vue'
import AdminDashboard from "./components/AdminDashboard.vue";
import ManagerDashboard from "./components/ManagerDashboard.vue";
import UserDashboard from "./components/UserDashboard.vue";
import AddCategory from "./components/Addcategory.vue";
import EditCategory from "./components/EditCategory.vue";
import CateGory from "./components/Category.vue";
import AddItem from "./components/Additem.vue";
import EditItem from "./components/EditItem.vue";
import ManagerItem from "./components/ManagerItem.vue";
import UserItem from "./components/UserItem.vue";
import SearcH from "./components/Search.vue";
import AllUser from "./components/AllUser.vue";
import CartItem from "./components/Cart.vue";


Vue.use(Router);

 const router = new Router({
    mode: 'history',
    routes:[
        { path: '/', component:HomePage },
        { path: '/login', component: LogIn },
        { path: '/register', component: RegisTer },
        { path: "/admin-dashboard", component: AdminDashboard, meta: { requiresAuth: true } },
        { path: "/manager-dashboard", component: ManagerDashboard, meta: { requiresAuth: true } },
        { path: "/user-dashboard", component: UserDashboard, meta: { requiresAuth: true } },
        { path: "/add-category", component: AddCategory },
        { path: "/edit-category/:id", component: EditCategory },
        { path: "/category", component: CateGory },
        { path: "/add-item", component: AddItem },
        { path: "/edit-item/:id", component: EditItem },
        { path: "/manager-item", component: ManagerItem },
        { path: "/user-item", component: UserItem },
        { path: "/search", name: 'search', component: SearcH },
        { path: "/all-user", component: AllUser },
        { path: "/cart", component: CartItem },

    ]
})






export default router;