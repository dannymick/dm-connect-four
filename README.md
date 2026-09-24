# DM Connect Four

## Instructions
```bash
# clone repo or use zip
cd dm-connect-four

# Install UV (https://docs.astral.sh/uv/getting-started/installation/#installation-methods)

# sync packages
uv sync

# run dev server, pyproject.toml points to main.py as entry point
uv run fastapi dev

# run tests
uv run pytest
```

Server: http://127.0.0.1:8000

Swagger docs: http://127.0.0.1:8000/docs