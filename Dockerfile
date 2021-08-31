FROM python:3.9

WORKDIR /home/youtube-bot
VOLUME /home/youtube-bot

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY .env .
COPY myyoutubeproject-292113-fcf735dc69cf.json .
COPY main.py .

ENTRYPOINT ["python", "main.py"]