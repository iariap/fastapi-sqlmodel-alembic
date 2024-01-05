# pull official base image
FROM python:3.12-slim-bookworm

# set working directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
# RUN apt-get update \
#   && apt-get -y install gcc postgresql \
#   && apt-get clean

# install python dependencies
RUN pip install --upgrade pip
COPY ./pyproject.toml .
RUN pip install .

# add app
COPY . .
