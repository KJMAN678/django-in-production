from django.contrib import admin


from author.models import Author, BlogAuthor


class AuthorAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "email", "created_at", "updated_at"]

class BlogAuthorAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "email", "created_at", "updated_at"]

admin.site.register(Author, AuthorAdmin)
admin.site.register(BlogAuthor, BlogAuthorAdmin)
