from django.contrib import admin

from author.models import Author


class AuthorAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "created_at", "updated_at"]


admin.site.register(Author, AuthorAdmin)
