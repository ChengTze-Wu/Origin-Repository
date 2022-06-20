FROM python:3.7-slim

WORKDIR /usr/src/taipei_oneday
COPY requirements.txt .
RUN pip install -r requirements.txt 

COPY . .