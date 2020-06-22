# -*- coding: utf-8 -*-

import requests
import uuid

from datetime import datetime, timedelta
from lxml import html


class Menu:

    def __init__(self):
        self.menu = {}
        self.current_date = datetime.today()
        self.DAYS = {
            'Montag': 0,
            'Dienstag': 1,
            'Mittwoch': 2,
            'Donnerstag': 3,
            'Freitag': 4,
            'Samstag': 5,
            'Sonntag': 6,
        }
        self.URL = 'http://derküchenmeister.de/?page_id=16'
        self.LOCATIONS = {
            'Montag': 'Maria-Reiche-Straße 1, 01109 Dresden Nanocenter',
            'Dienstag': 'Industriegelände, Firma haase-Businesstechnik GmbH, an der Handwerkskammer Dresden',
            'Mittwoch': 'Radebeul Seestraße 14, Parkplatz der Firma Feinkost Spina',
            'Donnerstag': 'Industriegelände, Firma haase-Businesstechnik GmbH, an der Handwerkskammer Dresden'
        }
        self.TIMES = {
            'Montag': ['10:30:00', '14:00:00'],
            'Dienstag': ['10:30:00', '14:00:00'],
            'Mittwoch': ['10:30:00', '13:30:00'],
            'Donnerstag': ['10:30:00', '14:00:00'],
        }

        self.parse_information()

    def parse_information(self):
        page = requests.get(self.URL)
        tree = html.fromstring(page.content)
        article = tree.xpath('//article[@id="post-16"]/div')[0]

        current_dishes = {}
        current_day = None
        current_meal = None

        for element in article:

            if element.tag == 'h3':
                self.create_dish(current_dishes, current_day)
                current_day = element.text
                current_dishes = {}
            if element.tag == "p" and element.text and current_day:
                text = element.text
                if text == ".":
                    continue
                elif text.startswith('-'):
                    current_meal = text[1:]
                    current_dishes[current_meal] = []
                else:
                    if current_meal:
                        current_dishes[current_meal].append(text)

        self.create_dish(current_dishes, current_day)

    def create_dish(self, current_dishes: dict, current_day: str):
        if current_dishes and current_day:
            dishes_list = []
            for dish, comments in current_dishes.items():
                offset = self.current_date.weekday() + self.DAYS[current_day]
                dishes_list.append(Dish({
                    'comments': comments,
                    'date': (self.current_date + timedelta(days=-offset)).strftime("%Y%m%d"),
                    'dish': dish,
                    'location': self.LOCATIONS[current_day],
                    'parse_date': self.current_date,
                    'supplier': "Küchi's Feldküche",
                    'time_from': self.TIMES[current_day][0],
                    'time_to': self.TIMES[current_day][1],
                }))
            self.menu[current_day] = dishes_list

    def create_slack_message(self):
        message_payload = {
            'text': '*%s*' % 'Küchis Speiseplan für diese Woche',
            'blocks': []
        }
        for day, dishes in self.menu.items():
            block = {
                'type': 'section',
                'text': {
                    'type': 'mrkdwn',
                    'text': f'*{day}:*\n{''.join([dish.create_slack_message() for dish in dishes])}\n'
                }
            }
            message_payload.get('blocks').append(block)
        return message_payload


class Dish:

    def __init__(self, values):
        self.id = values.get('id', self.generate_uuid())
        self.date = values.get('date', None)
        self.supplier = values.get('supplier', None)
        self.location = values.get('location', None)
        self.time_from = values.get('date', None)
        self.time_to = values.get('date', None)
        self.dish = self.escape_text(values.get('dish', None))
        self.comments = [self.escape_text(comment) for comment in values.get('comments', None)]

    @staticmethod
    def generate_uuid():
        return uuid.uuid4()

    @staticmethod
    def escape_text(text: str):
        return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

    def create_slack_message(self):
        if self.comments:
            return f'''- {self.dish}, _{' '.join([comment[0].lower() + comment[1:] for comment in self.comments])}_\n'''
        else:
            return f'''- {self.dish}\n'''


if __name__ == "__main__":
    menu = Menu()
    payload = menu.create_slack_message()
