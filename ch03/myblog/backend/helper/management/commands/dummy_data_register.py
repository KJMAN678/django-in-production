from blog.models import Blog
from blog.serializers import BlogSerializer
from author.serializers import AuthorSerializer
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Serializer のデータを登録する"

    def handle(self, *args, **options):
        input_author_data = {
            "name": "test",
            "email": "test@test.com",
            "bio": "this is bio",
        }
        new_author = AuthorSerializer(data=input_author_data)
        new_author.is_valid()
        new_author.save()
        author_id = new_author.data["id"]

        input_blog_data = {
            "title": "new blog title",
            "content": "this is content",
            "author": author_id,
        }
        # 登録
        new_blog = BlogSerializer(data=[input_blog_data, input_blog_data], many=True)
        print(new_blog.is_valid())
        new_blog.save()

        update_input_data = {
            "title": "updated blog title",
        }
        existing_blog = Blog.objects.latest("created_at")

        # 更新
        new_blog = BlogSerializer(
            instance=existing_blog, data=update_input_data, partial=True
        )
        new_blog.is_valid()
        new_blog.save()
