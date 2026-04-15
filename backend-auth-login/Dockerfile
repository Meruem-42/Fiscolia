FROM python:3.14-slim


WORKDIR /app

RUN apt update
RUN pip install fastapi uvicorn pydantic email_validator sqlalchemy psycopg2-binary

COPY ./config/ .

EXPOSE $BACK_AUTH_PORT

CMD [ "sh", "-c", "uvicorn response:auth --host 0.0.0.0 --port ${BACK_AUTH_PORT}" ]
