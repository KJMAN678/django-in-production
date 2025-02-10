from rest_framework.response import Response
from cacheops import cached
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
