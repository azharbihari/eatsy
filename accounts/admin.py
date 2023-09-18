from django.contrib import admin
from accounts.models import Account
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

User = get_user_model()


class AccountAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (("Profile", {"fields": [
        "date_of_birth", "bio", "avatar", "sex"]}),)


admin.site.register(User, AccountAdmin)


# Customize the default admin site attributes
admin.site.site_header = 'Eatsy Administration'
admin.site.index_title = 'Welcome to Eatsy Administration'
