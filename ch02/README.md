```sh
$ cd ch02/myblog
$ uv run django-admin startproject config backend/

$ docker compose up -d
$ docker compose build
```

### 公開されるサービスでは psycopg2-binary は使わないこと
https://www.psycopg.org/docs/install.html#psycopg-vs-psycopg-binary

http://localhost:8000/

```sh
$ mkdir backend/author
$ docker compose run --rm web uv run django-admin startapp author backend/author
$ mkdir backend/blog
$ docker compose run --rm web uv run django-admin startapp blog backend/blog
```

### model メモ
- blank=True/False はアプリケーション上の制約
- null=True/False はデータベース上の制約

### ダミーデータ登録
```sh
$ mkdir backend/helper
$ docker compose run --rm web uv run django-admin startapp helper backend/helper

$ docker compose run --rm web uv run backend/manage.py create_dummy_data

$ docker compose run --rm web uv run backend/manage.py done_query
```

### SQLで確認
- hostname は 127.0.0.1
- port は Dockerが指定している方 5432:5432 の前の方の 5432
```sql
# テーブル一覧
select schemaname, tablename, tableowner from pg_tables;

# データ取得
select * from blog_blog;
select * from author_author;
```

### ManyToManyModel で中間テーブルを指定する
https://docs.djangoproject.com/en/5.1/ref/models/fields/#django.db.models.ManyToManyField.through
https://qiita.com/mkizka/items/da4f8031d44fe1cdf353

### Proxy Model
https://docs.djangoproject.com/ja/5.1/topics/db/models/#proxy-models
https://tokibito.hatenablog.com/entry/2017/12/07/235805

### fake migration
```sh
$ docker compose run --rm web uv run backend/manage.py migrate author 0002 --fake
```

### TIMEZONE
https://docs.djangoproject.com/en/5.1/topics/i18n/timezones/

### Circular Dependency in models.py

- ForeignKeyの中身を文字列に変換すれば循環参照を回避できる

### Model Manager
https://docs.djangoproject.com/en/5.1/topics/db/managers/
- カスタムマネージャーを利用すると、複数のmodelで再利用できる共通のクエリロジックを作ることができる
- 下記の例では、Article.published.all() を呼び出すと、is_published=True の記事だけを取得できる
```python
from django.db import models

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    is_published = models.BooleanField(default=False)

    # カスタムマネージャーを設定
    objects = models.Manager()  # デフォルトマネージャー
    published = PublishedManager()  # カスタムマネージャー
```
- カスタムメソッドを追加できる
- 下記の例では Article.objects.recent_articles() で新着10件記事を表示できる
```python
    def recent_articles(self):
        return self.get_queryset().order_by('-created_at')[:10]

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    objects = ArticleManager()
```

### その他コマンド

```sh
$ docker compose run --rm web uv run backend/manage.py migrate
$ docker compose run --rm web uv run backend/manage.py makemigrations
$ docker compose run --rm web uv run backend/manage.py createsuperuser
```

### ruff によるコード整形
```sh
$ docker compose run --rm web uv run ruff check . --fix
$ docker compose run --rm web uv run ruff format .
```
