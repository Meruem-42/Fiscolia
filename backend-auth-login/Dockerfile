FROM python:3.14-slim


WORKDIR /app

RUN apt update
RUN pip install fastapi uvicorn pydantic email_validator

COPY ./response.py /app/response.py

EXPOSE 8000

CMD [ "uvicorn", "response:auth", "--host" , "0.0.0.0", "--port", "8000" ]
