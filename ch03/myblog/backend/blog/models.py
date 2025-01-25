import uuid
from django.db import models
from django.contrib import admin


class BaseTimeStampModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Blog(BaseTimeStampModel):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey("author.Author", on_delete=models.PROTECT)
    cover_image = models.OneToOneField(
        "CoverImage",
        # MEMO: これが blog_cover_image だとエラーになる
        related_name="cover_image",
        on_delete=models.PROTECT,
    )
    tags = models.ManyToManyField(
        "Tags",
    )

    def __str__(self):
        return self.title

    @admin.display
    def tag_names(self):
        return ", ".join([tag.name for tag in self.tags.all()])


class CoverImage(BaseTimeStampModel):
    image_link = models.URLField()

    def __str__(self):
        return self.image_link


class Tags(BaseTimeStampModel):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
