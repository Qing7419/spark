import { createRouter, createWebHistory } from "vue-router"

import UserLogin from "../components/UserLogin.vue"
import HeartPredict from "../components/HeartPredict.vue"

const routes = [

{
path:"/",
component:UserLogin
},

{
path:"/predict",
component:HeartPredict
}

]

const router = createRouter({
history:createWebHistory(),
routes
})

export default router