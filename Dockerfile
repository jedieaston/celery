FROM python:3.7
EXPOSE 8000
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
CMD gunicorn -w 4 app:app --bind 0.0.0.0:8000
