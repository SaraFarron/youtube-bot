FROM python:3.9

WORKDIR /home/youtube-bot

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY .env .
COPY myyoutubeproject-292113-fcf735dc69cf.json .
COPY *.py ./
