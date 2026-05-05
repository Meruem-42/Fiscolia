FROM python:3.11-slim


WORKDIR /app

RUN apt update
RUN pip install fastapi uvicorn pydantic email_validator sqlalchemy psycopg2-binary "passlib[bcrypt]" bcrypt==4.0.1

RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

RUN pip install --no-cache-dir \
    pandas \
    numpy \
    scikit-learn \
    matplotlib \
    seaborn \
    joblib

COPY ./config/ .

ARG BACK_AUTH_PORT
EXPOSE $BACK_AUTH_PORT

CMD [ "sh", "-c", "uvicorn main:auth --host 0.0.0.0 --port ${BACK_AUTH_PORT}" ]
