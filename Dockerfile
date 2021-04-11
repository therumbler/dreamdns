FROM python:3.8.5-alpine
RUN pip install --upgrade pip
RUN pip3 install pipenv

RUN mkdir /app
WORKDIR /app

COPY Pipfile* ./
RUN pipenv sync

COPY * ./
EXPOSE 8080
ENTRYPOINT pipenv run gunicorn -b 0.0.0.0:8080 --log-level DEBUG web:app
