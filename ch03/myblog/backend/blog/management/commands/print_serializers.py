from pprint import pprint

from blog.models import Blog
from blog.serializers import BlogSerializer, BlogCustom12Serializer
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

        # serializer 初期化中に context 引数を介して、すべてのシリアライザーメソッドで使用できる値を渡す事ができる
        input_data = BlogCustom12Serializer(
            data={"title": "abc"},
            context={"request": "some value"},
        )
        input_data.is_valid()
