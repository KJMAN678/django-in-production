import uuid
from django.db import models


class Author(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    demo_field = models.TextField(default="demo")
    email = models.EmailField()
    bio = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}-{self.id}"

    def get_author_name(self):
        return {self.name}

    def get_short_bio(self):
        return f"{self.bio[:200]}"

    class Meta:
        indexes = [models.Index(fields=["name"])]


class BlogAuthor(Author):
    class Meta:
        proxy = True

    def perform_something(self):
        pass
