# -*- coding: utf-8 -*-

# import subprocess
import requests

from menu import Menu

SLACK_HOOK_URL = ''

def post_message_to_slack():
    # message_payload = {
    #     'text': '*%s*' % SLACK_MESSAGE_TEXT,
    #     'attachments': [
    #         {
    #             'blocks': [
    #                 {
    #                     'type': 'image',
    #                     'image_url': '%s/%s' % (IMAGE_URL, IMAGE_NAME),
    #                     'alt_text': '%s' % SLACK_MESSAGE_TEXT
    #                 }
    #             ]
    #         }
    #     ]
    # }

    menu = Menu()
    message_payload = menu.create_slack_message()
    requests.post(SLACK_HOOK_URL, json=message_payload)


def main():
    # subprocess.call(['wkhtmltoimage', '--crop-h', '%s' % CROP_H, '--crop-w', '%s' % CROP_W, '--crop-x', '%s' % CROP_X, '--crop-y', '%s' % CROP_Y, KUECHI_MENU_URL, '%s%s' % (IMAGE_PATH, IMAGE_NAME)])
    post_message_to_slack()


if __name__ == "__main__":
    main()
