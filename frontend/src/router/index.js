import { createRouter, createWebHashHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import LoginView from "@/views/LoginView.vue";
import RegisterView from "@/views/RegisterView.vue";
import MyCourses from "@/views/MyCourses.vue";
import CoursePage from "@/views/CoursePage.vue";
import InstructorView from "@/views/InstructorView.vue";
import TaPage from "@/views/TaPage.vue";


const routes = [
  {
    path: "/",
    name: "home",
    component: HomeView,
  },
  {
    path: "/about",
    name: "about",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/AboutView.vue"),
  },
  {
    path: "/login",
    name: "login",
    component: LoginView,
  },
  {
    path: "/register",
    name: "register",
    component: RegisterView,
  },
  {
    path: "/mycourses",
    name: "mycourses",
    component: MyCourses,
  },
  {
    path: "/coursepage",
    name: "coursepage",
    component: CoursePage,
  },
  {
    path: "/instructor",
    name: "instructor",
    component: InstructorView,
  },
  {
    path: "/ta",
    name: "ta",
    component: TaPage,
  }
  
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

export default router;
