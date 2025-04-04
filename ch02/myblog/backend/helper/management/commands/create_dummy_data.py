from author.models import Author
from blog.models import Blog
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create dummy data for Author and Blog models"

    def handle(self, *args, **options):
        author_data = [
            {
                "name": "John Doe",
                "email": "john@gmail.com",
                "bio": "Python Blogger",
            },
            {
                "name": "Jane Doe",
                "email": "jane@gmail.com",
                "bio": "Django Blogger",
            },
        ]

        blog_data = [
            {
                "title": "Python is cool",
                "content": "Python is cool",
                "author": "john@gmail.com",
            },
            {
                "title": "Django is cool",
                "content": "Django is cool",
                "author": "jane@gmail.com",
            },
            {
                "title": "Django is better than Flask",
                "content": "Django is better than Flask",
                "author": "jane@gmail.com",
            },
        ]

        for author in author_data:
            Author.objects.get_or_create(email=author["email"], defaults={**author})

        for blog in blog_data:
            author = Author.objects.get(email=blog["author"])
            data = {**blog, "author": author}
            Blog.objects.get_or_create(title=blog["title"], defaults={**data})
