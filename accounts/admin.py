

# Register your models here.
from django.contrib import admin
from django.contrib.auth.models import Group

from .models import User

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


admin.site.register(User)  # Userモデルを登録
admin.site.unregister(Group)  # 非表示