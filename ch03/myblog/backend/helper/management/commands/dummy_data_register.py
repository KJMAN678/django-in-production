from blog.serializers import BlogSerializer, CoverImageSerializer, TagsSerializer
from author.serializers import AuthorSerializer
from django.core.management.base import BaseCommand
from django.db import transaction
from blog.models import Blog


class Command(BaseCommand):
    help = "Serializer のデータを登録する"

    @transaction.atomic
    def handle(self, *args, **options):
        input_author_data = [
            {
                "name": "test",
                "email": "test@test.com",
                "bio": "this is bio",
            },
            {
                "name": "test2",
                "email": "sample@sample.com",
                "bio": "this is sample bio",
            },
        ]
        new_author = AuthorSerializer(data=input_author_data, many=True)
        new_author.is_valid()
        new_author.save()
        author_ids = [data["id"] for data in new_author.data]

        input_cover_image_data = [
            {"image_link": "http://www.example.com"},
            {"image_link": "http://www.test.com"},
        ]
        new_cover_image = CoverImageSerializer(data=input_cover_image_data, many=True)
        new_cover_image.is_valid()
        new_cover_image.save()
        cover_image_ids = [data["id"] for data in new_cover_image.data]

        input_tags_data = [
            {"name": "tag1"},
            {"name": "tag2"},
        ]
        new_tags = TagsSerializer(data=input_tags_data, many=True)
        new_tags.is_valid()
        new_tags.save()

        input_blog_data = [
            {
                "title": "first blog title",
                "content": "this is content",
                "author": author_ids[0],
                "cover_image": cover_image_ids[0],
                "tags": [tag.id for tag in new_tags.instance],
            },
            {
                "title": "next blog title",
                "content": "excellent content is here",
                "author": author_ids[1],
                "cover_image": cover_image_ids[1],
                "tags": [tag.id for tag in new_tags.instance],
            },
        ]
        # 登録
        new_blog = BlogSerializer(data=input_blog_data, many=True)
        new_blog.is_valid()
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
