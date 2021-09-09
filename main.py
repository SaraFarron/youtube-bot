from logging import basicConfig, getLogger, INFO
from dotenv import load_dotenv
import schedule, time, json
from api_requests import get_last_videos


basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=INFO)
logger = getLogger(__name__)
load_dotenv()


def main():
    # channels = ['']  # TODO get all channels from db
    #
    # for channel in channels:
    #     schedule.every.day.at('1:00').do(get_last_videos(get_last_videos(channel, 5)))

    # while True:
    #     schedule.run_pending()
    #     time.sleep(60)

    response = get_last_videos('UCyzelLPcSrGUdLhN79eA4mg')
    with open('result.json', 'w', encoding='utf-8') as f:
        json.dump(response, f, ensure_ascii=False, indent=4)
        print('done')


if __name__ == '__main__':
    main()
