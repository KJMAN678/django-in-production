from django.db import models
from django.contrib import admin


class Blog(models.Model):
    title = models.CharField(max_length=100, unique=True)
    content = models.TextField()
    author = models.ForeignKey(
        "author.Author", related_name="author_blogs", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # MEMO: これが blog_cover_image だとエラーになる
    cover_image = models.OneToOneField(
        "CoverImage", related_name="cover_image", on_delete=models.CASCADE
    )
    tags = models.ManyToManyField("Tag", related_name="blog_tags")

    def __str__(self):
        return self.title

    @admin.display
    def tag_names(self):
        return ", ".join([tag.name for tag in self.tags.all()])


class BaseTimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CoverImage(BaseTimeStampModel):
    image_link = models.URLField()

    def __str__(self):
        return self.image_link


class Tag(BaseTimeStampModel):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
