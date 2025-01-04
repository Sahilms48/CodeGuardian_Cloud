FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install Django
RUN pip install -r requirements.txt
RUN pip install django-cors-headers
COPY . /app
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]