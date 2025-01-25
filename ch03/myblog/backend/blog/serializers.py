from rest_framework import serializers
from blog.models import Blog


class BlogSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        """create 関数をオーバーライドし、実行したことがわかるようにprint文を追加"""
        print("*** Custom Create method ***")
        return super(BlogSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        """update 関数をオーバーライドし、実行したことがわかるようにprint文を追加"""
        print("*** Custom Update method ***")
        return super(BlogSerializer, self).update(instance, validated_data)

    class Meta:
        model = Blog
        fields = "__all__"
