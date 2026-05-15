FROM python:3.14-slim

WORKDIR /app

RUN apt update
COPY tools/requirements.txt tools/requirements.txt
RUN pip install -r tools/requirements.txt

COPY ./config/ .


ARG BACK_CHATBOT_PORT
EXPOSE ${BACK_CHATBOT_PORT}

CMD ["sh", "-c", "uvicorn response_chatbot:app --host 0.0.0.0 --port ${BACK_CHATBOT_PORT}"]