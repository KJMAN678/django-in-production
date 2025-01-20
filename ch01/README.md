```sh
$ cd ch01/helloworld
$ uv run django-admin startproject config backend/

$ docker compose up -d
```
http://localhost:8000/demo-app/hello-world/

```sh
$ docker compose run --rm web uv run manage.py startapp demo_app
```

```sh
$ docker compose run --rm web uv run ruff check . --fix
$ docker compose run --rm web uv run ruff format .
```
