FROM python:3.6

EXPOSE 8000
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

CMD gunicorn -w 4 wsgi:app --bind 0.0.0.0:8000