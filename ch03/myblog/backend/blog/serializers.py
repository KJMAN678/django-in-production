from rest_framework import serializers
from blog.models import Blog, CoverImage, Tags
from author.models import Author
from rest_framework import validators

class BlogSerializer(serializers.ModelSerializer):
    # ForeignKey の対象のフィールドは, PrimaryKeyRelatedField で Serializer を指定する
    author = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all()
    )
    # ManyToManyField の対象のフィールドは, PrimaryKeyRelatedField を使い,
    # many=True, allow_empty=True を指定する
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tags.objects.all(),
        many=True,
        allow_empty=True,
    )
    # OneToOneField の対象のフィールドは, PrimaryKeyRelatedField を使い,
    # UniqueValidator を指定する
    cover_image = serializers.PrimaryKeyRelatedField(
        queryset=CoverImage.objects.all(),
        validators=[
            validators.UniqueValidator(
                queryset=CoverImage.objects.all(),
                message='重複！',
            )
        ]
    )

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


class CoverImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoverImage
        fields = "__all__"


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = "__all__"
