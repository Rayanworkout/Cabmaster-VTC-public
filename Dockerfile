FROM python:3

WORKDIR /app
COPY . /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN python cabmaster/manage.py makemigrations
RUN python cabmaster/manage.py migrate

EXPOSE 8000

CMD ["python", "cabmaster/manage.py", "runserver", "0.0.0.0:8000"]