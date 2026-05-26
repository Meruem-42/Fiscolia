FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

RUN pip install --no-cache-dir \
    pandas \
    numpy \
    scikit-learn \
    matplotlib \
    seaborn \
    joblib \
    sqlalchemy \
    psycopg2-binary

COPY training.py .
COPY get_secret.py .

CMD ["python", "training.py"]