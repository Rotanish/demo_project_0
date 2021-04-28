import Vue from "vue"
import VueRouter from "vue-router"
import Home from "@/views/Home.vue"

Vue.use(VueRouter)

const routes = [
  {
    path: "/secret",
    name: "Admin",
    component: () =>
      import("@/views/Admin.vue"),
  },
  {
    path: "/success",
    name: "success",
    component: () =>
      import("@/views/Success.vue"),
  },
  {
    path: "/fail",
    name: "fail",
    component: () =>
      import("@/views/Fail.vue"),
  },
  {
    path: "*",
    name: "Home",
    component: Home,
  },
]

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
})

export default router
