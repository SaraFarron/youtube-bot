from logging import basicConfig, getLogger, INFO, ERROR
from googleapiclient.discovery import build
from dotenv import load_dotenv
from os import environ
from time import sleep
import json

from db import (connect, create_table, insert,
                update, delete, get,
                )

basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=INFO)
logger = getLogger(__name__)
load_dotenv()

api_key = environ.get('GOOGL_API')
environ.get("GOOGLE_APPLICATION_CREDENTIALS")
number_of_videos_needed = 10

def main():
    youtube = build('youtube', 'v3', developerKey=api_key)

    request = youtube.search().list(
        part='snippet',
        channelId='UCyzelLPcSrGUdLhN79eA4mg',
        order='date',
        maxResults=number_of_videos_needed
    )
    # To get next page you need to take nextPageToken from results and make another request with added
    # PageToken = nextPageToken

    response = request.execute()
    with open('result.json', 'w', encoding='utf-8') as f:
        json.dump(response, f, ensure_ascii=False, indent=4)
        print('done')

if __name__ == '__main__':
    # main()
    # connect()
    insert('www.google.com', 'google', 'lol')
