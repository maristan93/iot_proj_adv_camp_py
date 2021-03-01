FROM python:3

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt 

COPY ./product ./product
COPY ./shop_app ./shop_app
COPY ./manage.py .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
