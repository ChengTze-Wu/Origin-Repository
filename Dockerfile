FROM python:3.7-slim

WORKDIR /usr/src/taipei_day_trip
COPY requirements.txt .
RUN pip install -r requirements.txt 

COPY . .

EXPOSE 8000

CMD ["gunicorn"]