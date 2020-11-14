from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'nickname', 'email', 'first_name', 'last_name', 'is_staff')

    def nickname(self, obj):
        return obj.profile.nickname
    nickname.short_description = '昵称'


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


# 上面的代码可以让一个用户有多个昵称，django官方文档
# https://docs.djangoproject.com/en/2.0/topics/auth/customizing/
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'nickname')
