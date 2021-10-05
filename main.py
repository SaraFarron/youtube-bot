from logging import basicConfig, getLogger, INFO
import json
from api_requests import get_last_videos


basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=INFO)
logger = getLogger(__name__)


def main():

    response = get_last_videos('UCyzelLPcSrGUdLhN79eA4mg')
    with open('result.json', 'w', encoding='utf-8') as f:
        json.dump(response, f, ensure_ascii=False, indent=4)
        print('done')


if __name__ == '__main__':
    main()
