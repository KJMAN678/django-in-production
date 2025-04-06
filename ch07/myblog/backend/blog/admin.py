from django.contrib import admin
from blog.models import Blog, CoverImage, Tag


class BlogAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "author",
        "cover_image",
        "tag_names",
        "created_at",
        "updated_at",
    )
    list_select_related = ("author", "cover_image")


class CoverImageAdmin(admin.ModelAdmin):
    list_display = ("image_link", "created_at", "updated_at")


class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at", "updated_at")


admin.site.register(Blog, BlogAdmin)
admin.site.register(CoverImage, CoverImageAdmin)
admin.site.register(Tag, TagAdmin)
