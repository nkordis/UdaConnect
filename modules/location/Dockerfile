FROM python:3.9-slim-buster

WORKDIR .

RUN apt-get update && apt-get install -y build-essential libgeos-dev libpq-dev

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "consumer.py"]

