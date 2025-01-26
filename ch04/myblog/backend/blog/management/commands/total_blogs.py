from django.core.management.base import BaseCommand
from blog.models import Blog


class Command(BaseCommand):
    help = "Returns total number of blogs"

    def handle(self, *args, **options):
        total_blogs = Blog.objects.count()
        print(total_blogs)
