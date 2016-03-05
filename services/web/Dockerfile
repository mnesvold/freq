FROM python:3.5
ENV PYTHONUNBUFFERED 1
RUN pip install --upgrade pip
ADD ./requirements.txt /srv/
WORKDIR /srv
RUN pip install -r requirements.txt
