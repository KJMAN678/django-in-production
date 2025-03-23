```sh
# 初回のみ ディレクトリ作成、プロジェクト作成
$ cd ch07-ex01-pagenator/myblog

- 前の章の pyproject.toml、docker関連ファイルを myblog ディレクトリ直下にコピーする
- 前の章の backend ディレクトリを myblog ディレクトリ直下にコピーする

$ mkdir logs
```

```sh
# ディレクトリ構成
ch07-ex01-pagenator/ --- myblog/ --- backend/ --- config/
       |           |
       |           |- logs/
       |           |- docker-compose.yaml
       |           |- Dockerfile
       |           |- pyproject.toml
       |           |- uvlock.lock
       |
       |- README.md
```

```sh
# 環境変数を読み込んで Docker立上げ
$ docker compose --env-file ../../.env up --detach
# Docker再ビルド
$ docker compose --env-file ../../.env build

$ docker compose --env-file ../../.env exec web uv run backend/manage.py migrate
# superuser 作成. 設定は docker-compose.yaml で設定した環境変数から読み込む
# WARN は表示されるが登録はできる
# カスタムユーザーモデルを利用しており、ユーザーを pnohe_no で識別しているので phone_no を別途設定している
$ docker compose --env-file ../../.env exec web uv run backend/manage.py createsuperuser --noinput

# ダミーデータの登録
$ docker compose --env-file ../../.env exec web uv run backend/manage.py dummy_data_register

# キャッシュの削除
$ docker builder prune -f
```
- author_id が 1のブログを取得
http://127.0.0.1:8000/blog/blogs_auto_invalidation/?author_id=1
http://127.0.0.1:8000/blog/blogs_anon_view/
http://127.0.0.1:8000/blog/blogs_user_view/
http://127.0.0.1:8000/blog/blogs_scoped_view/

- def log_event() でログを記録する
http://127.0.0.1:8000/blog/blogs_logs/?author_id=1

- ページネーション比較用, ページネーションのないブログ一覧
http://127.0.0.1:8000/blog/unpaginated/
- ページネーションのあるブログ一覧
http://127.0.0.1:8000/blog/paginated/?page=1&page_size=1
- DjangoのPagenatorを使ったページネーションのあるブログ一覧
http://127.0.0.1:8000/blog/django_paginator/?page=1&page_size=1

- DRFのページネーション
http://127.0.0.1:8000/blog/get_blogs/?limit=10&offset=1

http://127.0.0.1:8000/admin/login/


### ページネーションをHTMLデザイン含めてやってみる
- d

### その他コマンド

```sh
$ docker compose --env-file ../../.env exec web uv run backend/manage.py migrate
$ docker compose --env-file ../../.env exec web uv run backend/manage.py makemigrations
# superuser 作成. 設定は docker-compose.yaml で設定した環境変数から読み込む
# WARN は表示されるが登録はできる
$ docker compose --env-file ../../.env exec web uv run backend/manage.py createsuperuser --noinput

# app 追加. settings の INSTALLED_APPS も更新
$ mkdir backend/blog
$ docker compose --env-file ../../.env exec web uv run django-admin startapp blog backend/blog

# 環境変数の確認
$ docker compose --env-file ../../.env exec web env

# コンテナに入る
$ docker container exec -it web bash
```

### ruff によるコード整形
```sh
$ docker compose --env-file ../../.env exec web uv run ruff check . --fix
$ docker compose --env-file ../../.env exec web uv run ruff format .
```
