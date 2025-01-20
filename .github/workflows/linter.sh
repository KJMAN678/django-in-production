name: linter
on: [pull_request]

jobs:
  build:

    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.10"]

    steps:
      - uses: actions/checkout@v3
      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      - name: library install
        run: |
          pip install --upgrade pip
          pip install ruff==0.1.6 mypy==1.7.1
      - name: Lint with ruff
        run: |
          ruff check --target-version=py310 --output-format=github .
      - name: Lint with mypy 
        run: |
          mypy .
