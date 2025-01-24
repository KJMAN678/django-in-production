from blog.serializers import BlogSerializer
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Serializer の中身を確認する"

    def handle(self, *args, **options):
        print(BlogSerializer())
