from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, \
    PasswordResetView, PasswordChangeDoneView, PasswordResetCompleteView, PasswordResetConfirmView, \
    PasswordResetDoneView
from .views import user_login, dashboard_view, logout_page, logout_view, SignUpView, user_register, edit_user, \
    EditUserView

urlpatterns = [
    # path('login/', user_login, name='login'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_page, name="logout"),
    path('profile/', dashboard_view, name='user_profile'),
    path('password-change/', PasswordChangeView.as_view(), name="password_change"),
    path('password-change-done/', PasswordChangeDoneView.as_view(), name="password_change_done"),
    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset/complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('signup/', user_register, name='user_register'),
    # path('profile/edit/', edit_user, name='edit_user_information'),
    path('profile/edit/', EditUserView.as_view(), name='edit_user_information'),

    # path('signup/', SignUpView.as_view(), name="user_register"),
]