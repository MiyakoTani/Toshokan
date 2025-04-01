from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django import forms
from django.forms import ModelForm
from .models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
        )
        labels={
           "username":"ユーザーネーム",
            "email":"メールアドレス",
            "first_name":"名",
            "last_name":"姓",
           }

# ログインフォーム
class LoginForm(AuthenticationForm):
    class Meta:
        model = User

'''パスワード変更フォーム'''
class MyPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class UserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
        )
        labels={
           "username":"ユーザーネーム",
            "email":"メールアドレス",
            "first_name":"名",
            "last_name":"姓",
           }

class UserDeleteForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            "is_active",
        )
        labels={
           'is_active':'ユーザーを有効化',
           }

class StaffAccountsChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "is_active",
            "is_staff",
        )
        labels={
           "username":"ユーザーネーム",
            "email":"メールアドレス",
            "first_name":"名",
            "last_name":"姓",
            'is_active':'ユーザーを有効化',
            'is_staff':'管理者権限',
           }
        
class ForgetForm(forms.Form):
    choice = forms.ChoiceField(
        label="分からない方を選択してください。",
        choices=(
            ('un','ユーザーネーム'),
            ('pw','パスワード'),
        ),
        initial = "un",
        widget=forms.RadioSelect(),
    )

class UsernameForm(ModelForm):
    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
        )
        labels={
            "email":"メールアドレス",
            "first_name":"名",
            "last_name":"姓",
           }