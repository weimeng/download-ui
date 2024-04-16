FROM python:alpine

RUN pip install --no-cache-dir gallery-dl flask

COPY . /download-ui/

CMD cd download-ui && flask --app download-ui run --host=0.0.0.0
