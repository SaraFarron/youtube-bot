from googleapiclient.discovery import build
from dotenv import load_dotenv
from os import environ

load_dotenv()

api_key = environ.get('GOOGL_API')
environ.get("GOOGLE_APPLICATION_CREDENTIALS")

youtube = build('youtube', 'v3', developerKey=api_key)

request = youtube.channels().list(
        part='statistics',
        forUsername='schafer5'
    )

response = request.execute()

print(response)