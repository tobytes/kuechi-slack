# -*- coding: utf-8 -*-

import requests
import urllib.request

KUECHI_MENU_URL = 'http%3A%2F%2Fderk%C3%BCchenmeister.de%2F%3Fpage_id%3D16menu'
KUECHI_MENU_ELEMENT = '.site-main'

SLACK_HOOK_URL = ''
SLACK_MESSAGE_TEXT = 'Küchis Speiseplan für diese Woche'

IMAGE_URL = ''
IMAGE_PATH = ''
IMAGE_NAME = 'kuechi_menu.jpg'

APIFLASH_ACCESS_KEY = ''


def post_message_to_slack():
    message_payload = {
        'text': '*%s*' % SLACK_MESSAGE_TEXT,
        'attachments': [
            {
                'blocks': [
                    {
                        'type': 'image',
                        'image_url': '%s/%s' % (IMAGE_URL, IMAGE_NAME),
                        'alt_text': '%s' % SLACK_MESSAGE_TEXT
                    }
                ]
            }
        ]
    }

    requests.post(SLACK_HOOK_URL, json=message_payload)


def main():
    urllib.request.urlretrieve('https://api.apiflash.com/v1/urltoimage?access_key=%s&element=%s&format=jpeg&response_type=image&url=%s' % (APIFLASH_ACCESS_KEY, KUECHI_MENU_ELEMENT, KUECHI_MENU_URL), '%s%s' % (IMAGE_PATH, IMAGE_NAME))
    post_message_to_slack()


if __name__ == "__main__":
    main()
