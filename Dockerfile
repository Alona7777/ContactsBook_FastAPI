FROM python:3.11-slim

# RUN pip install poetry

WORKDIR .

# COPY pyproject.toml .
# COPY poetry.lock .

# RUN poetry shell
# RUN poetry install 
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install uvicorn

COPY . .

CMD [“alembic”, “upgrade”, “heads”]

ENTRYPOINT ["python", "main.py"]

  