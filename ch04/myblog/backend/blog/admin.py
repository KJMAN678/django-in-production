from django.contrib import admin
from blog.models import Blog
from django.contrib.admin.models import LogEntry
from django.core import paginator
from django.utils.functional import cached_property


class CustomPaginator(paginator.Paginator):
    @cached_property
    def count(self):
        return 9999999


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
    # ページネーション機能を追加
    paginator = CustomPaginator
    # 外部キー制約のあるフィールドを選択する際に、リスト選択ではなく、入力フォーム形式にする
    raw_id_fields = ["author"]
    # N+1問題対策
    list_select_related = ["author"]

    # カスタムフィールドとして list_display に追加可能
    def word_count(self, obj):
        return obj.content.split()

    def get_queryset(self, request):
        default_queryset = super().get_queryset(request)
        improved_queryset = default_queryset.select_related("author")
        return improved_queryset

    # Admin で実行できるアクションを追加.
    actions = ("print_blogs_titles",)

    @admin.action(description="タイトルを表示")
    def print_blogs_titles(self, request, queryset):
        for data in queryset.all():
            print(data.title, flush=True)


admin.site.register(Blog, BlogAdmin)
admin.site.register(LogEntry, LogEntryAdmin)
