from django.contrib import admin
from blog.models import Blog, CoverImage, Tags


class BlogAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "content",
        "cover_image",
        "tag_names",
        "created_at",
        "updated_at",
    ]


class CoverImageAdmin(admin.ModelAdmin):
    list_display = ["id", "image_link", "created_at", "updated_at"]


class TagsAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "created_at", "updated_at"]


admin.site.register(Blog, BlogAdmin)
admin.site.register(CoverImage, CoverImageAdmin)
admin.site.register(Tags, TagsAdmin)
