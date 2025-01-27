from django.contrib import admin

from author.models import Author


class AuthorAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "bio"]


admin.site.register(Author, AuthorAdmin)
