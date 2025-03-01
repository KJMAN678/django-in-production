from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from demo_app import custom_versions


@api_view(["GET"])
def hello_world_drf(request, *args, **kwargs):
    return Response(data={"message": "Hello, World!"})


@api_view(["GET"])
def demo_version(request, *args, **kwargs):
    version = request.version
    return Response(data={"msg": f"You have hit {version} of demo-api"})


class DemoView(APIView):
    """class ベースの APIView を使用して、バージョン管理を行う"""

    # v1, v2, v3 以外のバージョンが指定された場合は 404 を返す
    versioning_class = custom_versions.DemoViewVersion

    def get(self, request, *args, **kwargs):
        version = request.version
        return Response(data={"msg": f"You have hit {version}"})


class AnotherView(APIView):
    # v1, v2 のリクエストがあるたびに異なるレスポンスを返す
    versioning_class = custom_versions.AnotherViewVersion

    def get(self, request, *args, **kwargs):
        version = request.version
        if version == "v1":
            # perform v1 related tasks
            return Response(data={"msg": "v1 logic"})
        elif version == "v2":
            # perform v2 related tasks
            return Response(data={"msg": "v2 logic"})


class DemoAPIView(APIView):
    def get(self, request, *args, **kwargs):
        return Response(data={"msg": "get request block"})

    def post(self, request, *args, **kwargs):
        return Response(data={"msg": "post request block"})

    def delete(self, request, *args, **kwargs):
        return Response(data={"msg": "delete request block"})
