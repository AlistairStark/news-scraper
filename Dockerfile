FROM python:3.8-slim-buster

WORKDIR /app

RUN apt-get update

# Install packages
RUN apt-get install -y \
  libpq-dev \
  python3-psycopg2 \
  python3-dev \
  gcc

COPY requirements.txt requirements.txt

EXPOSE 5000

RUN pip install -r requirements.txt

CMD [ "run.sh" ]