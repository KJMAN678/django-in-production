from blog.serializers import BlogSerializer, CoverImageSerializer, TagsSerializer
from author.serializers import AuthorSerializer
from django.core.management.base import BaseCommand
from django.db import transaction
from blog.models import Blog


class Command(BaseCommand):
    help = "Serializer のデータを登録する"

    @transaction.atomic
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

        input_cover_image_data = {
            "image_link": "http://www.example.com",
        }
        new_cover_image = CoverImageSerializer(data=input_cover_image_data)
        new_cover_image.is_valid()
        new_cover_image.save()
        cover_image_id = new_cover_image.data["id"]

        input_tags_data = [
            {"name": "tag1"},
            {"name": "tag2"},
        ]
        new_tags = TagsSerializer(data=input_tags_data, many=True)
        print(new_tags.is_valid())
        new_tags.save()

        input_blog_data = {
            "title": "new blog title",
            "content": "this is content",
            "author": author_id,
            "cover_image": cover_image_id,
            "tags": [tag.id for tag in new_tags.instance],
        }
        # 登録
        new_blog = BlogSerializer(data=input_blog_data)
        if new_blog.is_valid():
            new_blog.save()
            print("Blog created successfully")
        else:
            print(new_blog.errors)

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
