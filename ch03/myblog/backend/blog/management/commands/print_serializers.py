from pprint import pprint

from blog.models import Blog
from blog.serializers import BlogSerializer
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Serializer の中身を確認する"

    def handle(self, *args, **options):
        print(BlogSerializer())

        # 表示
        last_obj = Blog.objects.latest("created_at")
        blog_obj = BlogSerializer(instance=last_obj)
        pprint(blog_obj.data)

        multiple_blogs = Blog.objects.all()
        blog_objs = BlogSerializer(instance=multiple_blogs, many=True)
        pprint(blog_objs.data)
