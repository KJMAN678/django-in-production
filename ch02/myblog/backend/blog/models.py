import uuid
from django.db import models
from author.models import Author


class Blog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(
        Author, related_name="author_blogs", on_delete=models.PROTECT
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class BaseTimeStampModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CoverImage(BaseTimeStampModel):
    image_link = models.URLField()
    blog = models.OneToOneField(Blog, related_name="blog_ci", on_delete=models.PROTECT)


class DemoModel(BaseTimeStampModel):
    name = models.CharField(max_length=100)
