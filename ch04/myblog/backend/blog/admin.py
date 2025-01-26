from django.contrib import admin
from blog.models import Blog
from django.contrib.admin.models import LogEntry


# @admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    """has_<action>_permission メソッドをオーバーライドして、読み取り専用にしている"""

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False


class BlogAdmin(admin.ModelAdmin):
    # 検索フォームの対象フィールド
    search_fields = ["title"]

    # 1ページあたりの表示件数の表示
    show_full_result_count = True

    # フィルター候補を挙げフィルター機能として使える
    list_filter = ["title"]

    # 一覧表示のフィールド
    list_display = ["id", "title", "word_count", "created_at"]

    # 階層化したリンク
    date_hierarchy = "created_at"

    # ManyTOManyField の UI を改善する
    # # 利用可能な tag一覧と、選択されたタグ一覧を横並びで表示する
    filter_horizontal = ["tags"]
    # 縦並びで表示するパターン
    # filter_vertical = ["tags"]

    # カスタムフィールドとして list_display に追加可能
    def word_count(self, obj):
        return obj.content.split()

    def get_queryset(self, request):
        default_queryset = super().get_queryset(request)
        improved_queryset = default_queryset.select_related("author")
        return improved_queryset


admin.site.register(Blog, BlogAdmin)
admin.site.register(LogEntry, LogEntryAdmin)
