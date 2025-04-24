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
    path('accounts_delete/', views.DeactivateUser, name='delete'), # ユーザー削除
    path('staff_search_user/<int:page>', views.staff, name='staff'), 
    path('staff_accounts_change/<str:num>', views.StaffAccountsChange, name='staff_accounts_change'), 
    path('forget', views.ForgetView.as_view(), name='forget'), 
    path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'), #追加
    path('password_reset_done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'), #追加
    path('password_reset_confirm/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'), #追加
    path('password_reset_complete/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'), #追加
    path('username_reset/', views.UsernameResetView.as_view(), name='username_reset'), #追加
    path('username_reset_done/', views.UsernameResetDoneView.as_view(), name='username_reset_done'),
    path('borrowing_history/<int:page>', views.borrowing_history, name='borrowing_history'),
    path('review/<int:pk>/', views.my_review_detail, name='my_review')
]