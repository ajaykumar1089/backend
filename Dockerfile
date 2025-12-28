#backend/Dockerfile
FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app


COPY requirements.txt .
RUN  pip intall  --no-cache-dir -r requirements.txt

COPY . . 
RUN python manage.py collectstatic --noinput 
CMD ["gunicorn", "--bind", "0.0.0.0:8000","myapp.wsgi:applicaton"]
