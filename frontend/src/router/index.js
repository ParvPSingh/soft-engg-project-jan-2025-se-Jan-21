import { createRouter, createWebHashHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import LoginView from "@/views/LoginView.vue";
import RegisterView from "@/views/RegisterView.vue";

import MyCourses from "@/views/MyCourses.vue";
import CoursePage from "@/views/CoursePage.vue";
import InstructorView from "@/views/InstructorView.vue";
import TaPage from "@/views/TaPage.vue";
import TaQuery from "@/views/TaQuery.vue";
import WeeklyPerformance from "@/views/WeeklyPerformance.vue";
import PractiseAssignmnet from "@/views/PractiseAssignmnet.vue";
import ProgrammingAssignmnet from "@/views/ProgrammingAssignmnet.vue";
import AboutView from "@/views/AboutView.vue";


import TADashboardView from '@/views/TADashboardView.vue';

import SupplymentaryContent from "@/views/SupplymentaryManage.vue";
import InstructorFeedback from "@/views/InstructorFeedback.vue";
import StudentQueries from "@/views/StudentQueries.vue";
import ManageStudents from "@/views/ManageStudents.vue";
const routes = [
  
  {
    path: "/",
    name: "home",
    component: HomeView,
  },
  // {
  //   path: "/about",
  //   name: "about",
  //   // route level code-splitting
  //   // this generates a separate chunk (about.[hash].js) for this route
  //   // which is lazy-loaded when the route is visited.
  //   component: () =>
  //     import(/* webpackChunkName: "about" */ "../views/AboutView.vue"),
  // },
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
    meta: { role: "student" }
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
    meta: { role: "instructor" }
  },
  {
    path: "/ta",
    name: "ta",
    component: TaPage,
    meta: { role: "ta" }
  },
  {
    path: "/taquery",
    name: "taquery",
    component: TaQuery,
  },
  {
    path: "/weeklyperformance",
    name: "weeklyperformance",
    component: WeeklyPerformance,
  },
  {
    path: "/prassignment",
    name: "prassignment",
    component: PractiseAssignmnet,
  },
  {
    path: "/prgassignment",
    name: "prgassignment",
    component: ProgrammingAssignmnet,
  },
  {
  
    path: "/ta-dashboard",
    name: "TADashboard",
    component: TADashboardView
  },
  {
    path: "/aboutpage",
    name: "aboutpage",
    component: AboutView
  },

  {
    path: "/supplymentary",
    name: "SupplymentaryContent",
    component: SupplymentaryContent
  },
  {
    path: "/feedback",
    name: "InstructorFeedback",
    component: InstructorFeedback
  },
  {
    path: "/studentqueries",
    name: "studentqueries",
    component: StudentQueries
  },
  {
    path: "/managestudents",
    name: "managestudents",
    component: ManageStudents

  }

];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const user = JSON.parse(localStorage.getItem("user")); // Get user from storage
  const requiredRole = to.meta.role; // Get required role from route meta

  if (requiredRole) {
    if (!user || user.role.toLowerCase() !== requiredRole.toLowerCase()) {
      alert("Access Denied! You do not have permission to view this page.");
      return next("/"); // Redirect unauthorized users to homepage
    }
  }
  next();
});

export default router;
