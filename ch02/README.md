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
$ docker compose run --rm web uv run backend/manage.py startapp demo_app
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
