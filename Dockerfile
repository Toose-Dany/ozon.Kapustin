FROM python:3.12-slim

WORKDIR /src
COPY ["./", "./"]

RUN pip install --no-cache-dir psycopg2-binary fastapi uvicorn

CMD ["uvicorn", "main:app", "--reload","--host","0.0.0.0", "--port","8080"]