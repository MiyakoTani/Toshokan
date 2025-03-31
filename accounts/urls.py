from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path('signup/', views.SignupView.as_view(), name="signup"),
    path('logout/', views.LogoutView.as_view(), name="logout"),
    path('password_change/', views.PasswordChange.as_view(), name='password_change'), # パスワード変更
    path('password_change_done/', views.PasswordChangeDone.as_view(), name='password_change_done'), # パスワード変更完了
    path('change/', views.UserChangeView.as_view(), name="change"),# ユーザー編集
    path('accounts_delete/', views.UserDeleteView.as_view(), name='delete'), # ユーザー削除
    path('accounts/staff_search_user', views.staff, name='staff'), 
    path('accounts/staff_accounts_change/<str:num>', views.StaffAccountsChange, name='staff_accounts_change'), 
]