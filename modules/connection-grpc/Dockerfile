FROM python:3.9

WORKDIR .

RUN apt-get update && apt-get install -y build-essential libgeos-dev libpq-dev

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["python", "server.py"]
