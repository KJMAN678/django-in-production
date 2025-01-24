```sh
# 初回のみ ディレクトリ作成、プロジェクト作成
$ cd ch01/helloworld
$ uv run django-admin startproject config backend/

# 環境変数を読み込んで Docker立上げ
$ docker compose --env-file ../../.env up --detach
# Docker再ビルド
$ docker compose --env-file ../../.env build
```
### DRFのパス
### migrate が必要
http://localhost:8000/demo-app/hello-world-drf/
http://localhost:8000/v1/demo-app-version/demo-version/

### v4 は選択できないので 404 not found となる
http://localhost:8000/v4/demo-app-version/custom-version/

### v1 と v2 で異なるメッセージを返す
http://localhost:8000/v1/demo-app-version/another-custom-version/
http://localhost:8000/v2/demo-app-version/another-custom-version/
```sh
$ docker compose exec web uv run django-admin startapp demo_app
```

### router について
https://www.django-rest-framework.org/api-guide/routers/

### class based view
http://localhost:8000/v1/demo-app-version/apiview-class/

### ViewSets
https://www.django-rest-framework.org/api-guide/viewsets/

### その他コマンド

```sh
$ docker compose exec web uv run backend/manage.py migrate
$ docker compose exec web uv run backend/manage.py makemigrations
# superuser 作成. 設定は docker-compose.yaml で設定した環境変数から読み込む
# WARN は表示されるが登録はできる
$ docker compose exec web uv run backend/manage.py createsuperuser --noinput
```

### ruff によるコード整形
```sh
$ docker compose exec web uv run ruff check . --fix
$ docker compose exec web uv run ruff format .
```
