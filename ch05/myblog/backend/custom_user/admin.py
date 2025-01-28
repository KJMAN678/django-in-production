from django.contrib import admin

# from custom_user.models import CustomUser

from django.contrib.admin.models import LogEntry


class LogEntryAdmin(admin.ModelAdmin):
    """has_<action>_permission メソッドをオーバーライドして、読み取り専用にしている"""

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False


# class CustomUserAdmin(UserAdmin):
#     model = CustomUser
#     list_display = ["id", "phone_no", "city", "is_staff", "is_superuser"]
#     readonly_fields = ["is_superuser"]
#     filter_horizontal = ["groups", "user_permissions"]
#     # 下記のエラーに対応
#     # <class 'custom_user.admin.CustomUserAdmin'>: (admin.E033)
#     # The value of 'ordering[0]' refers to 'username', which is not a field of 'custom_user.CustomUser'.
#     fieldsets = ((None, {"fields": ("phone_no", "password")}),)
#     ordering = ("phone_no",)


# admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(LogEntry, LogEntryAdmin)
