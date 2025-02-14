from rest_framework.response import Response
from cacheops import cached, cached_as
from rest_framework.decorators import api_view

from blog.models import Blog
from blog.serializers import BlogSerializer


@cached(timeout=60 * 10)
def get_all_blogs(author_id):
    print("Fetching blogs from database")
    blogs = Blog.objects.filter(author_id=author_id)
    blogs_data = BlogSerializer(blogs, many=True).data
    return blogs_data


@api_view(["GET"])
def get_blogs_by_author(request):
    # ?author=xxx のパラメータの取得
    author_id = request.GET.get("author_id")
    blogs = get_all_blogs(author_id)
    return Response({"blogs": blogs})


# settings.py で CACHEOPS = {"blog.blog": {"ops": "all", "timeout": xxx},} を設定した場合は、
# @cached_as(Blog) とするだけでキャッシュが有効になり、自動でキャッシュが無効化される
# 空の{}とするか、殻ではないが blog.blog の設定がない場合はエラーとなる

@cached_as(Blog, timeout=60 * 10)
def get_all_blogs_auto_invalidation(author_id):
    blogs = Blog.objects.filter(author_id=author_id)
    blogs_data = BlogSerializer(blogs, many=True).data
    return blogs_data


@api_view(["GET"])
def get_blogs_by_author_auto_invalidation(request):
    # ?author=xxx のパラメータの取得
    author_id = request.GET.get("author_id")
    blogs = get_all_blogs_auto_invalidation(author_id)
    return Response({"blogs": blogs})
