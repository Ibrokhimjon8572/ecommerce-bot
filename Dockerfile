FROM python:3.10 as builder

WORKDIR /app

RUN python -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

COPY ./requirements.txt ./requirements.txt

RUN pip install -r requirements.txt



FROM python:3.10

WORKDIR /app

ENV PATH="/opt/venv/bin:$PATH"

COPY --from=builder /opt/venv /opt/venv

COPY ./src /app/src/


EXPOSE 8000

RUN uvicorn myproject.asgi:application --host 0.0.0.0 --port 8000 --reload 