from django.contrib import admin
from blog.models import Blog


class BlogAdmin(admin.ModelAdmin):
    pass


admin.site.register(Blog, BlogAdmin)
