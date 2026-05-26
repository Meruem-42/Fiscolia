FROM python:3.11-slim


WORKDIR /app

RUN apt update
RUN pip install pandas requests

COPY . .
RUN chmod 777 ./*
CMD [ "python3", "create_profile.py" ]
