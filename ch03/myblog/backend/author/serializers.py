from rest_framework import serializers
from author.models import Author


class AuthorSerializer(serializers.ModelSerializer):
    long_bio = serializers.CharField(source="bio", read_only=True)
    short_bio = serializers.CharField(source="fetch_short_bio", read_only=True)

    class Meta:
        model = Author
        fields = "__all__"
