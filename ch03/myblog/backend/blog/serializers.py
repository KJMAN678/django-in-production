from rest_framework import serializers
from blog.models import Blog, CoverImage, Tags
from author.models import Author
from rest_framework import validators


class BlogSerializer(serializers.ModelSerializer):
    # ForeignKey の対象のフィールドは, PrimaryKeyRelatedField で Serializer を指定する
    author = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all())
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
        # MEMO: Blog モデルの cover_image フィールドのrelated_name を blog_cover_image に変更すると、
        # 下記のエラーになる
        # django.core.exceptions.FieldError: Cannot resolve keyword 'cover_image'
        # into field. Choices are: blog_cover_image, created_at, id, image_link, updated_at
        validators=[
            validators.UniqueValidator(
                queryset=CoverImage.objects.all(),
            )
        ],
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
        fields = [
            "id",
            "title",
            "content",
            "author",
            "cover_image",
            "tags",
            "created_at",
            "updated_at",
        ]


class CoverImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoverImage
        fields = "__all__"


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = "__all__"


class BASerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["name", "bio"]


class BlogCustomSerializer(serializers.ModelSerializer):
    author_details = BASerializer(source="author")

    class Meta:
        model = Blog
        fields = "__all__"


class BlogCustom2Serializer(serializers.ModelSerializer):
    word_count = serializers.SerializerMethodField()

    def get_word_count(self, obj):
        """メソッドの名前は get_<field name> とする必要がある"""
        return len(obj.content.split())

    class Meta:
        model = Blog
        fields = "__all__"


class BlogCustom3Serializer(serializers.ModelSerializer):
    """メソッド名を get_<field name>以外にする場合は、引数 method_name で指定する必要あり"""

    word_count = serializers.SerializerMethodField(method_name="use_custom_word_count")

    def use_custom_word_count(self, obj):
        return len(obj.content.split())

    class Meta:
        model = Blog
        fields = "__all__"


class BlogCustom4Serializer(serializers.ModelSerializer):
    # validate_<field name> というメソッドを定義すると、
    # is_valid() メソッドが呼び出されるたびに実行される.
    def validate_title(self, value):
        """
        タイトル内にアンダースコアが含まれている場合は、is_valid()実行時にエラーを発生させる
        """
        print("validate_title method")
        if "_" in value:
            raise serializers.ValidationError("illegal char")
        raise value

    class Meta:
        model = Blog
        fields = "__all__"


# Meta クラスの extra_kwargs で、各フィールドに対してバリデーションを追加することもできる
def demo_func_validator(attr):
    print("func val")
    if "_" in attr:
        raise serializers.ValidationError("illegal char")
    return attr


class BlogCustom5Serializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = "__all__"
        extra_kwargs = {
            "title": {
                "validators": [demo_func_validator],
            },
            "content": {
                "validators": [demo_func_validator],
            },
        }


# Meta クラスの validators に関数を指定することで、全体のバリデーションを追加する
class BlogCustom6Serializer(serializers.ModelSerializer):
    def validate(self, attrs):
        if attrs["title"] == attrs["content"]:
            raise serializers.ValidationError("Title and content cannot have value")
        return attrs

    class Meta:
        model = Blog
        fields = "__all__"


def custom_obj_validator(attrs):
    print("custom object validator")
    if attrs["title"] == attrs["content"]:
        raise serializers.ValidationError("Title and content cannot have the same")
    return attrs


class BlogCustom7Serializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = "__all__"
        validators = [custom_obj_validator]


def func_validator(attr):  # 最初に呼ばれる
    print("func val")
    if "*" in attr:
        raise serializers.ValidationError("Illegal char")
    return attr


class BlogCustom8Serializer(serializers.ModelSerializer):
    def validate_title(self, value):  # 2番目に呼ばれる
        print("validate_title method")
        if "_" in value:
            raise serializers.ValidationError("Illegal char")
        return value

    def validate(self, attrs):  # 3番目に呼ばれる
        print("main validate method")
        return attrs

    class Meta:
        model = Blog
        fields = "__all__"
        extra_kwargs = {
            "title": {
                "validators": [func_validator],
            }
        }


# Meta クラスの validators に空リストを指定することで、全体のバリデーションを無効にする
class BlogCustom9Serializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = "__all__"
        validators = []


# to_internal_value メソッドをオーバーライドすることで、データのバリデーション前に処理を追加できる
class BlogCustom10Serializer(serializers.ModelSerializer):
    def to_internal_value(self, data):
        print("before validation data", data)
        return super().to_internal_value(data)

    class Meta:
        model = Blog
        fields = "__all__"


# to_representation メソッドをオーバーライドすることで、Model オブジェクト　を Python 型に変換する前に処理を追加できる
class BlogCustom11Serializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        resp = super().to_representation(instance)
        resp["title"] = resp["title"].upper()
        return resp

    class Meta:
        model = Blog
        fields = "__all__"


# serializer 初期化中に context 引数を介して、すべてのシリアライザーメソッドで使用できる値を渡す事ができる
class BlogCustom12Serializer(serializers.ModelSerializer):
    def to_internal_value(self, data):
        print("Printing context -", self.context)
        return super().to_internal_value(data)

    class Meta:
        model = Blog
        fields = "__all__"


# 作成者が作成したタグのみをブログに追加できるようにしたい.
# context と カスタムフィールドの概念を利用して実行できる
# CustomPKRelatedField を作成し、デフォルトの get_queryset メソッドをオーバーライドする
# CustomPKRelatedField は、リクエストされたユーザーが作成したタグを自動的にフィルタリングし、
# ユーザーが作成していないタグを選択できないようにする
class CustomPKRelatedField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        # context value
        req = self.context.get("request", None)
        # retrieve default filter
        queryset = super().get_queryset()
        if not req:
            return None
        return queryset.filter(user=req.user)


# additional filter
class BlogCustom13Serializer(serializers.ModelSerializer):
    tags = CustomPKRelatedField(queryset=Tags.objects.all())

    class Meta:
        model = Blog
        fields = "__all__"
