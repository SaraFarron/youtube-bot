from googleapiclient.discovery import build
from dotenv import load_dotenv
from os import environ
from time import sleep
import json

from db import (connect, create_table, insert,
                insert_many, update, delete,
                get,
                )


load_dotenv()

api_key = environ.get('GOOGL_API')
environ.get("GOOGLE_APPLICATION_CREDENTIALS")

def main():
    youtube = build('youtube', 'v3', developerKey=api_key)

    request = youtube.search().list(
        part='snippet',
        channelId='UCyzelLPcSrGUdLhN79eA4mg',
        order='date',
    )

    response = request.execute()
    with open('result.json', 'w', encoding='utf-8') as f:
        json.dump(response, f, ensure_ascii=False, indent=4)
        print('done')

if __name__ == '__main__':
    # main()
    # connect()
    insert(('идти', 'go'), 'words')
    insert_many([
        ('стоять', 'stand'),
        ('класть', 'put')
    ], 'words')
