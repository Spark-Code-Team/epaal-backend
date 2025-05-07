FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y build-essential libpq-dev libjpeg-dev zlib1g-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY requirements.txt /code/
RUN pip install --upgrade pip --timeout 350 && pip install -r requirements.txt --timeout 350

COPY . /code/

RUN mkdir -p /vol/web/static /vol/web/media

CMD ["gunicorn", "Loana.wsgi:application", "--bind", "0.0.0.0:8000"]