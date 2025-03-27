from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path('signup/', views.SignupView.as_view(), name="signup"),
    path('logout/', views.LogoutView.as_view(), name="logout"),
    path('password_change/', views.PasswordChange.as_view(), name='password_change'), # パスワード変更
    path('password_change_done/', views.PasswordChangeDone.as_view(), name='password_change_done'), # パスワード変更完了
    #path('change/', views.UserChangeView.as_view(), name="change"),# パスワード変更
]