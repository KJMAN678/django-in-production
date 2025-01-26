```sh
# 初回のみ ディレクトリ作成、プロジェクト作成
$ cd ch04/myblog
$ uv run django-admin startproject config backend/

# 環境変数を読み込んで Docker立上げ
$ docker compose --env-file ../../.env up --detach
# Docker再ビルド
$ docker compose --env-file ../../.env build

$ docker compose exec web uv run backend/manage.py migrate
# superuser 作成. 設定は docker-compose.yaml で設定した環境変数から読み込む
# WARN は表示されるが登録はできる
$ docker compose exec web uv run backend/manage.py createsuperuser --noinput
```
http://localhost:8000/index/
http://localhost:8000/admin/login/

```sh
$ mkdir backend/blog
$ docker compose exec web uv run django-admin startapp blog backend/blog
$ mkdir backend/author
$ docker compose exec web uv run django-admin startapp author backend/author
$ mkdir backend/helper
$ docker compose exec web uv run django-admin startapp helper backend/helper
```

### Serializer による レコード登録
- Tag はユニーク制約があり、一度しか登録できない点に注意.
```sh
$ docker compose exec web uv run backend/manage.py dummy_data_register
```

### awesome-django-admin
https://github.com/originalankur/awesome-django-admin

### Json 表示用ヴィジェット
https://github.com/jmrivas86/django-json-widget

### Django Custom Command
```sh
$ docker compose exec web uv run backend/manage.py total_blogs
$ docker compose exec web uv run backend/manage.py custom_command_info 12 45 --custom 99
```

### その他コマンド

```sh
$ docker compose exec web uv run backend/manage.py migrate
$ docker compose exec web uv run backend/manage.py makemigrations
# superuser 作成. 設定は docker-compose.yaml で設定した環境変数から読み込む
# WARN は表示されるが登録はできる
$ docker compose exec web uv run backend/manage.py createsuperuser --noinput

# 環境変数の確認
$ docker compose exec web env
$ docker compose --env-file ../../.env exec web env
```

### ruff によるコード整形
```sh
$ docker compose exec web uv run ruff check . --fix
$ docker compose exec web uv run ruff format .
```
