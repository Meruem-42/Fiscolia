FROM python:3.11-slim


WORKDIR /app

RUN apt update
RUN pip install requests

COPY . .
RUN chmod 777 ./*

CMD [ "python3", "create_user.py" ]
