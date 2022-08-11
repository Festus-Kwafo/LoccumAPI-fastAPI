#Pull base image
FROM python:3.9

#set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#work directory
WORKDIR /loccumapi-fastapi

# install system dependencies
RUN apt-get update \
  && apt-get -y install netcat gcc postgresql \
  && apt-get clean

# Install dependencies
RUN pip install --upgrade pip
COPY requirements.txt /loccumapi-fastapi/
RUN pip install -r requirements.txt

# Copy project
COPY . /loccumapi-fastapi/