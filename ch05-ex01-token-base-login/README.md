```sh
# 初回のみ ディレクトリ移動
$ cd ch05/myblog

### フロントエンド
# 初回のみ プロジェクト作成
$ npx create-next-app@latest frontend/ --ts --eslint --tailwind --src-dir --use-npm --app --turbopack --no-import-alias

### バックエンド
$ uv run django-admin startproject config backend/

# 環境変数を読み込んで Docker立上げ
$ docker compose --env-file ../../.env up --detach
# Docker再ビルド
$ docker compose --env-file ../../.env build

$ docker compose exec web uv run backend/manage.py migrate
# superuser 作成. 設定は docker-compose.yaml で設定した環境変数から読み込む
# WARN は表示されるが登録はできる
$ docker compose exec web uv run backend/manage.py createsuperuser --noinput

# キャッシュの削除
$ docker builder prune
```
### フロントエンド
http://127.0.0.1:3000/

### バックエンド
http://127.0.0.1:8000/account/login/
http://127.0.0.1:8000/account/logout/
http://127.0.0.1:8000/account/logoutall/

http://127.0.0.1:8000/admin/login/

```sh
$ mkdir backend/blog
$ docker compose --env-file ../../.env exec backend uv run django-admin startapp blog backend/blog
$ mkdir backend/author
$ docker compose --env-file ../../.env exec backend uv run django-admin startapp author backend/author
$ mkdir backend/helper
$ docker compose --env-file ../../.env exec backend uv run django-admin startapp helper backend/helper
$ mkdir backend/account
$ docker compose --env-file ../../.env exec backend uv run django-admin startapp account backend/account
```

### ダミーデータの登録
```sh
$ docker compose --env-file ../../.env exec backend uv run backend/manage.py dummy_data_register
```

### django-rest-knox を使う
https://github.com/jazzband/django-rest-knox
https://jazzband.github.io/django-rest-knox/auth/

### その他コマンド

```sh
# フロントエンド
# install した node_modules フォルダの削除
$ docker compose --env-file ../../.env exec frontend rm -rf node_modules

# JavaScript ライブラリのインストール
$ docker compose --env-file ../../.env exec frontend npm install

# package-json, package-json-lock のアプデ
$ docker compose --env-file ../../.env exec frontend npx npm-check-updates -u
$ docker compose --env-file ../../.env exec frontend npm install

# バックエンド
$ docker compose --env-file ../../.env exec backend uv run backend/manage.py migrate
$ docker compose --env-file ../../.env exec backend uv run backend/manage.py makemigrations
# superuser 作成. 設定は docker-compose.yaml で設定した環境変数から読み込む
# WARN は表示されるが登録はできる
$ docker compose --env-file ../../.env exec backend uv run backend/manage.py createsuperuser --noinput

# 環境変数の確認
$ docker compose --env-file ../../.env exec backend env
```

### コード整形
```sh
# フロントエンド
# ESLint の実行
$ docker compose --env-file ../../.env exec frontend npm run lint

# バックエンド
$ docker compose --env-file ../../.env exec backend uv run ruff check ./backend --fix
$ docker compose --env-file ../../.env exec backend uv run ruff format ./backend
```
