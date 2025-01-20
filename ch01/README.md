```sh
$ cd ch01/helloworld
$ uv run django-admin startproject config backend/

$ docker compose up -d
$ docker compose build
```
### DRFのパス
### migrate が必要
http://localhost:8000/demo-app/hello-world-drf/

```sh
$ docker compose run --rm web uv run backend/manage.py startapp demo_app
```

```sh
$ docker compose run --rm web uv run backend/manage.py migrate
$ docker compose run --rm web uv run backend/manage.py makemigrations
$ docker compose run --rm web uv run backend/manage.py createsuperuser
```

```sh
$ docker compose run --rm web uv run ruff check . --fix
$ docker compose run --rm web uv run ruff format .
```
