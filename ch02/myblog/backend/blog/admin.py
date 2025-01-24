from blog.models import Blog, CoverImage, DemoModel
from django.contrib import admin


class BlogAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "author", "created_at", "updated_at"]


class CoverImageAdmin(admin.ModelAdmin):
    list_display = ["id", "image_link", "created_at", "updated_at"]


class DemoModelAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "created_at", "updated_at"]


admin.site.register(Blog, BlogAdmin)
admin.site.register(CoverImage, CoverImageAdmin)
admin.site.register(DemoModel, DemoModelAdmin)
