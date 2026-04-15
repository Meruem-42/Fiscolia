FROM python:3.14-slim

WORKDIR /app

RUN apt update
COPY tools/requirements.txt tools/requirements.txt
RUN pip install -r tools/requirements.txt

COPY ./config/ /app/

EXPOSE 8001

CMD [ "uvicorn", "response_chatbot:app", "--host" , "0.0.0.0", "--port", "8001" ]