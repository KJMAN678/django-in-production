poetry run ruff --format=github --select=E9,F63,F7,F82,I --target-version=py310 . --fix
poetry run pytest .
