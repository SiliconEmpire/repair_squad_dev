from django.urls import path
from django.contrib.auth import views as auth_views
from . import views as users_views

urlpatterns = [
    path('register/', users_views.registerView, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    # path('profile/', users_views.profile, name='profile'),
    path('profile/', users_views.ProfileView.as_view(), name='profile'),
    path('profile-update/', users_views.profile_update_view, name='profile_update'),
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='users/password_reset.html'
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='users/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='users/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='users/password_reset_complete.html'
         ),
         name='password_reset_complete'),
    # path('profile-update/', users_views.profile_update_view, name='profile_update'),
]
