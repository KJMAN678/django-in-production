from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes


@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    username = request.data["username"]
    password = request.data["password"]
    user = authenticate(username=username, password=password)
    if not user:
        return Response(status="401")
    token, _ = Token.objects.get_or_create(user=user)
    return Response(data={"token": token.key})
