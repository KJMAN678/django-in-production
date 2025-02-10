```sh
# 初回のみ ディレクトリ作成、プロジェクト作成
$ cd ch06/myblog
$ uv run django-admin startproject config backend/

# 環境変数を読み込んで Docker立上げ
$ docker compose --env-file ../../.env up --detach
# Docker再ビルド
$ docker compose --env-file ../../.env build

$ docker compose --env-file ../../.env exec web uv run backend/manage.py migrate
# superuser 作成. 設定は docker-compose.yaml で設定した環境変数から読み込む
# WARN は表示されるが登録はできる
# カスタムユーザーモデルを利用しており、ユーザーを pnohe_no で識別しているので phone_no を別途設定している
$ docker compose --env-file ../../.env exec web uv run backend/manage.py createsuperuser --noinput

# キャッシュの削除
$ docker builder prune -f
```
- author_id が 1のブログを取得
http://127.0.0.1:8000/blog/blogs/?author_id=1

http://127.0.0.1:8000/admin/login/


```sh
$ mkdir backend/blog
$ docker compose --env-file ../../.env exec web uv run django-admin startapp blog backend/blog
$ mkdir backend/author
$ docker compose --env-file ../../.env exec web uv run django-admin startapp author backend/author
$ mkdir backend/helper
$ docker compose --env-file ../../.env exec web uv run django-admin startapp helper backend/helper
```

### ダミーデータの登録
```sh
$ docker compose --env-file ../../.env exec web uv run backend/manage.py dummy_data_register
```

### Cache の確認コマンド
```sh
$ docker compose --env-file ../../.env exec web uv run backend/manage.py print_cache
```
- ビューごとのキャッシュ
https://docs.djangoproject.com/en/5.1/topics/cache/#the-per-view-cache
- Django RestFramework Caching
https://www.django-rest-framework.org/api-guide/caching/

### django-cacheops
https://github.com/Suor/django-cacheops
- ORM クエリを自動キャッシュしてくれたり, 色々キャッシュ周りを自動化してくれるらしい.

- invalidate でキャッシュを削除することもできる
https://github.com/Suor/django-cacheops?tab=readme-ov-file#invalidation

```python
# author ID 12 のキャッシュを削除
get_all_blogs.invalidate(12)

# すべてキャッシュを削除
get_all_blogs.invalidate()
```

### その他コマンド

```sh
$ docker compose --env-file ../../.env exec web uv run backend/manage.py migrate
$ docker compose --env-file ../../.env exec web uv run backend/manage.py makemigrations
# superuser 作成. 設定は docker-compose.yaml で設定した環境変数から読み込む
# WARN は表示されるが登録はできる
$ docker compose --env-file ../../.env exec web uv run backend/manage.py createsuperuser --noinput

# 環境変数の確認
$ docker compose --env-file ../../.env exec web env
```

### ruff によるコード整形
```sh
$ docker compose --env-file ../../.env exec web uv run ruff check . --fix
$ docker compose --env-file ../../.env exec web uv run ruff format .
```

docker exec -it 3f2b7fd4bafd04db1ac34974aa696e5f4d82169753a41b00dba8e40f045d4f0e redis-cli
