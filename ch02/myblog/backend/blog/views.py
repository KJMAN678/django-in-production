from django.http import JsonResponse

from blog.models import Blog


def get_blog(request):
    blog_details = Blog.objects.get(id="acb4fa66-dca0-45cc-a224-dd77762e6cb4")
    return JsonResponse(
        {
            "title": blog_details.title,
        }
    )


async def async_get_blog(request):
    blog_details = await Blog.objects.aget(id="acb4fa66-dca0-45cc-a224-dd77762e6cb4")
    return JsonResponse(
        {
            "title": blog_details.title,
        }
    )
