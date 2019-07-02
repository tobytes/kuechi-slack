# -*- coding: utf-8 -*-

import subprocess
import requests

KUECHI_MENU_URL = 'http://derküchenmeister.de/?page_id=16'
SLACK_HOOK_URL = ''
SLACK_MESSAGE_TEXT = 'Küchis Speiseplan für diese Woche'

IMAGE_URL = ''
IMAGE_PATH = ''
IMAGE_NAME = 'kuechi_menu.jpg'


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
    subprocess.call(['wkhtmltoimage', KUECHI_MENU_URL, '%s%s' % (IMAGE_PATH, IMAGE_NAME)])
    post_message_to_slack()


if __name__ == "__main__":
    main()
