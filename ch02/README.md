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
