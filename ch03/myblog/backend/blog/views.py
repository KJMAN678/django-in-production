from rest_framework import views
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework import filters


from blog.models import Blog
from blog.serializers import BlogSerializer


class BlogGetCreateView(views.APIView):
    def get(self, request):
        blogs_obj_list = Blog.objects.all()
        blogs = BlogSerializer(
            blogs_obj_list,
            many=True,
        )
        return Response(blogs.data)

    def post(self, request):
        input_data = request.data
        b_obj = BlogSerializer(data=input_data)
        if b_obj.is_valid():
            b_obj.save()
            return Response(b_obj.data, status=status.HTTP_201_CREATED)
        return Response(b_obj.errors, status=status.HTTP_400_BAD_REQUEST)


class BlogGetUpdateView(generics.ListCreateAPIView):
    serializer_class = BlogSerializer

    def get_queryset(self):
        queryset = Blog.objects.filter(title__contains="updated")
        return queryset


class BlogGetUpdateFilterView(generics.ListAPIView):
    serializer_class = BlogSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["title"]

    def get_queryset(self):
        queryset = Blog.objects.filter(title__contains="updated")
        return queryset
