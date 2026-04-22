FROM python:3.14-slim


WORKDIR /app

RUN apt update
RUN pip install fastapi uvicorn python-multipart

COPY ./config/ .

EXPOSE $UPLOAD_PORT

CMD [ "sh", "-c", "uvicorn upload:app --host 0.0.0.0 --port ${UPLOAD_PORT}" ]