```sh
$ cd ch01/helloworld
$ uv run django-admin startproject config backend/

$ docker compose up -d
$ docker compose build
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
$ docker compose run --rm web uv run backend/manage.py startapp demo_app
```

### router について
https://www.django-rest-framework.org/api-guide/routers/

### class based view
http://localhost:8000/v1/demo-app-version/apiview-class/

### ViewSets
https://www.django-rest-framework.org/api-guide/viewsets/

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
