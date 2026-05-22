FROM python:3.12-slim

WORKDIR /app

RUN mkdir -p ma_base_chroma

RUN apt-get update -y && apt-get clean

COPY tools/requirements.txt tools/

RUN pip install -r tools/requirements.txt

COPY . .

CMD ["python", "create_vector_db.py"]