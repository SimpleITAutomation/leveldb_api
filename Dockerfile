# pull official base image
FROM python:3.9.4-alpine

WORKDIR /code/

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . /code

# install dependencies
RUN set -eux \
    && apk add --no-cache --virtual .build-deps build-base \
        libressl-dev libffi-dev gcc musl-dev python3-dev leveldb-dev \
    && pip install --upgrade pip setuptools wheel \
    && pip install -r /code/requirements.txt \
    && rm -rf /root/.cache/pip

ENV PYTHONPATH=/code

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
