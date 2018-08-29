FROM ubuntu:16.04
RUN apt-get update && apt-get install python3 python3-pip -y
EXPOSE 8000
WORKDIR /app
COPY . .
COPY wait.sh /
RUN pip3 install --no-cache-dir -r requirements.txt
CMD gunicorn -w 4 app:app --bind 0.0.0.0:8000