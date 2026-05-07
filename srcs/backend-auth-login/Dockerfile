FROM python:3.14-slim


WORKDIR /app

RUN apt update
RUN pip install fastapi uvicorn pydantic email_validator sqlalchemy psycopg2-binary "passlib[bcrypt]" bcrypt==4.0.1

COPY ./config/ .

ARG BACK_AUTH_PORT
EXPOSE $BACK_AUTH_PORT

CMD [ "sh", "-c", "uvicorn main:auth --host 0.0.0.0 --port ${BACK_AUTH_PORT}" ]
