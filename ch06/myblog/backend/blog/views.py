from rest_framework.response import Response
from cacheops import cached, cached_as
from rest_framework.decorators import api_view
from rest_framework import views
from rest_framework.throttling import (
    AnonRateThrottle,
    UserRateThrottle,
    ScopedRateThrottle,
)

from blog.models import Blog
from blog.serializers import BlogSerializer
from common.logging_util import log_event


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
    log_event("get_blogs_by_author", {"author_id": author_id})
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


class BlogAnonAPIView(views.APIView):
    # throttele_classes はすべてのスロットルクラスのリストを保持する
    # AnonRateThrottle は匿名ユーザーに対するスロットルクラス
    throttele_classes = [AnonRateThrottle]

    def get(self, request):
        blogs_obj_list = Blog.objects.all()
        blogs = BlogSerializer(
            blogs_obj_list,
            many=True,
        )
        return Response(blogs.data)


class BlogUserAPIView(views.APIView):
    # throttele_classes はすべてのスロットルクラスのリストを保持する
    # UserRateThrottle は認証ユーザーに対するスロットルクラス
    throttele_classes = [UserRateThrottle]

    def get(self, request):
        blogs_obj_list = Blog.objects.all()
        blogs = BlogSerializer(
            blogs_obj_list,
            many=True,
        )
        return Response(blogs.data)


class BlogScopedAPIView(views.APIView):
    # throttele_classes はすべてのスロットルクラスのリストを保持する
    # throttele_scope は、settings.py の REST_FRAMEWORK/DEFAULT_THROTTLE_RATES で
    # 設定したカスタムのスロットルスコープを指定することができる
    throttele_classes = [ScopedRateThrottle]
    throttele_scope = "blog_limit"

    def get(self, request):
        blogs_obj_list = Blog.objects.all()
        blogs = BlogSerializer(
            blogs_obj_list,
            many=True,
        )
        return Response(blogs.data)
