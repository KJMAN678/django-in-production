from author.models import Author
from blog.models import Blog
from django.core.management.base import BaseCommand
from django.db import connection
from helper.db_debug import database_debug


@database_debug
def reqular_query():
    blogs = Blog.objects.all()
    return [blog.author.name for blog in blogs]


@database_debug
def select_related_query():
    blogs = Blog.objects.select_related("author").all()
    return [blog.author.name for blog in blogs]


@database_debug
def prefetch_related_query():
    blogs = Blog.objects.prefetch_related("author").all()
    return [blog.author.name for blog in blogs]


class Command(BaseCommand):
    help = "Create dummy data for Author and Blog models"

    def handle(self, *args, **options):
        author_obj = Blog.objects.get(id="acb4fa66-dca0-45cc-a224-dd77762e6cb4").author
        print(author_obj)

        author = Author.objects.get(email="john@gmail.com")
        all_blogs_by_an_author = author.author_blogs.all()
        print(all_blogs_by_an_author)

        selected_blog = author.author_blogs.filter(title="Python is cool")
        print(selected_blog)

        all_authors = (
            Author.objects.filter(email__endswith="@gmail.com")
            .values_list("name")
            .query
        )
        print(all_authors)

        author_count = Author.objects.filter(email="a").count()
        print(author_count)
        # DEBUG = True のときのみ利用可能
        print(connection.queries[-1])

        print(
            Blog.objects.filter(title="Python is cool").explain(
                verbose=True, analyze=True
            )
        )

        some_query = Blog.objects.filter(
            author__id="acb4fa66-dca0-45cc-a224-dd77762e6cb4"
        )
        another_query = some_query.filter(author__name__startswith="J")
        yet_another_query = another_query.filter(author__name__endswith="e")
        print(yet_another_query)

        reqular_query()
        select_related_query()
        prefetch_related_query()
