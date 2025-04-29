import AppLayout from '@/views/pages/AppLayout.vue';
import { createRouter, createWebHistory } from 'vue-router';
import { ApiService } from '@/services/api';

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/',
            component: AppLayout,
            children: [
                {
                    path: '/pages/empty',
                    name: 'empty',
                    component: () => import('@/views/pages/Empty.vue')
                },
                {
                    path: '/admin',
                    name: 'admin',
                    component: () => import('@/views/pages/Admin.vue'),
                    meta: { requiresAdmin: true },
                },
                {
                    path: '/dashboard',
                    name: 'dashboard',
                    component: () => import('@/views/pages/Dashboard.vue')
                },
                {
                    path: '/generate-event',
                    name: 'generate-event',
                    component: () => import('@/views/pages/Generate-event.vue')
                },
                {
                    path: '/events',
                    name: 'events',
                    component: () => import('@/views/pages/Events.vue')
                },
                {
                    path: '/my-events',
                    name: 'my-events',
                    component: () => import('@/views/pages/Events.vue')
                },
                {
                    path: '/artists',
                    name: 'artists',
                    component: () => import('@/views/pages/Artists.vue')
                },
                {
                    path: '/concerthalls',
                    name: 'concerthalls',
                    component: () => import('@/views/pages/Concerthalls.vue')
                },
                {
                    path: '/tracks',
                    name: 'tracks',
                    component: () => import('@/views/pages/Tracks.vue')
                },
            ]
        },
        {
            path: '/pages/notfound',
            name: 'notfound',
            component: () => import('@/views/pages/NotFound.vue')
        },
        {
            path: '/auth/login',
            name: 'login',
            component: () => import('@/views/pages/auth/Login.vue')
        },
        {
            path: '/auth/register',
            name: 'register',
            component: () => import('@/views/pages/auth/Register.vue')
        },
        {
            path: '/auth/access',
            name: 'accessDenied',
            component: () => import('@/views/pages/auth/Access.vue')
        },
        {
            path: '/auth/error',
            name: 'error',
            component: () => import('@/views/pages/auth/Error.vue')
        }
    ]
});

router.beforeEach(async (to, from, next) => {
    const token = localStorage.getItem('authToken');
    const publicPages = ['/auth/login', '/auth/register/', '/auth/error', '/auth/access'];
    const authRequired = !publicPages.includes(to.path);

    if (authRequired && !token) {
        return next('/auth/login');
    }

    if (to.meta.requiresAdmin) {
        try {
            const response = await ApiService.get('/profile/');
            const user = response.data;

            localStorage.setItem('userProfile', JSON.stringify(user));

            if (user.role === 'admin') {
                return next();
            } else {
                return next('/auth/access');
            }
        } catch (error) {
            console.error('Error fetching user profile:', error);
            return next('/auth/access');
        }
    }

    next();
});



export default router;
