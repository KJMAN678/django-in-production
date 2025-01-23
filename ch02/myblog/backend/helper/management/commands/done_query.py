from author.models import Author
from blog.models import Blog
from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = "Create dummy data for Author and Blog models"

    def handle(self, *args, **options):
        author_obj = Blog.objects.get(id=1).author
        print(author_obj)

        author = Author.objects.get(email="john@gmail.com")
        all_blogs_by_an_author = author.blog_set.all()
        print(all_blogs_by_an_author)

        selected_blog = author.blog_set.filter(title="Python is cool")
        print(selected_blog)

        all_authors = (
            Author.objects.filter(email__endswith="@gmail.com")
            .values_list("name")
            .query
        )
        print(all_authors)

        author_count = Author.objects.filter(email="a").count()
        print(author_count)
        print(connection.queries[-1])
