FROM python:3.7.4
ENV PYTHONUNBUFFERED 1
RUN mkdir /forum
WORKDIR /forum
ADD requirements.txt /forum/
RUN pip install -r requirements.txt
ADD . /django-docker/