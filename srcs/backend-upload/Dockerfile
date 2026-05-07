FROM python:3.14-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libxcb1 \
    libxcb-render0 \
    libxcb-shape0 \
    libxcb-xfixes0 \
    libgl1 \
    libglib2.0-0 \
    tesseract-ocr \
    tesseract-ocr-fra \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir fastapi uvicorn python-multipart pymupdf docling

COPY ./config/ .

EXPOSE $BACK_UPLOAD_PORT

CMD ["sh", "-c", "uvicorn upload:app --host 0.0.0.0 --port ${BACK_UPLOAD_PORT}"]