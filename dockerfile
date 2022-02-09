# pull official base image
FROM python

# set work directory
WORKDIR /usr/src/API

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apt update
RUN apt install python3-pip python3-dev libpq-dev -y

# install dependencies
RUN pip install --upgrade pip
COPY ./API/requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .