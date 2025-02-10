from django.core.cache import cache
from django.core.management.base import BaseCommand
from django.core.cache import caches


class Command(BaseCommand):
    help = "Cache のデータを登録、出力する"

    def handle(self, *args, **options):
        cache.set("hello", "World", 600)
        print(cache.get("hello"))
        print(caches["default"].__class__)
