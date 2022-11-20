import re
from typing import Dict
from bs4 import BeautifulSoup
from bs4.element import Tag


class CollectData:
    def __init__(self, src: BeautifulSoup):
        self.src = src

    def get_title(self):
        try:
            return self.src.find('h1', {'class': 'ember-view'}).text.split('\n')[1]
        except Exception as ex:
            #print(f'[INFO] No title in card, {ex}')
            return 'no_info'

    @staticmethod
    def get_overview(card_path):
        try:
            return card_path.find('p').text
        except Exception as ex:
            #print(f'[INFO] No overview in card, {ex}')
            return 'no_info'

    def get_location(self):
        try:
            return re.sub(r'\n', '', self.src.find('div', {'class': 'org-location-card pv2'}).find('p').text).strip()
        except Exception as ex:
            #print(f'[INFO] No location in card, {ex}')
            return 'no_info'

    def get_followers(self):
        try:
            return re.findall(r'[0-9]+', self.src.find('div', {'class': 'inline-block'}).
                              find_all('div', {'class': 'org-top-card-summary-info-list__info-item'})[-1].text)[0]
        except Exception as ex:
            #print(f'[INFO] No followers in card, {ex}')
            return 'no_info'

    @staticmethod
    def get_website(card_data: Dict) -> str:
        for key, value in card_data.items():
            if key.lower() != 'website':
                continue
            return value
        return 'no_info'

    @staticmethod
    def get_phone(card_data: Dict) -> str:
        for key, value in card_data.items():
            if key.lower() != 'phone':
                continue
            return value.split('  ')[0]
        return 'no_info'

    @staticmethod
    def get_industry(card_data: Dict) -> str:
        for key, value in card_data.items():
            if key.lower() != 'industry':
                continue
            return value
        return 'no_info'

    @staticmethod
    def get_company_size(card_data: Dict) -> str:
        for key, value in card_data.items():
            if key.lower() != 'company size':
                continue
            return value.split('  ')[0]
        return 'no_info'

    @staticmethod
    def get_headquarters(card_data: Dict) -> str:
        for key, value in card_data.items():
            if key.lower() != 'headquarters':
                continue
            return value
        return 'no_info'

    @staticmethod
    def get_founded(card_data: Dict) -> str:
        for key, value in card_data.items():
            if key.lower() != 'founded':
                continue
            return value
        return 'no_info'

    @staticmethod
    def get_specialties(card_data: Dict) -> str:
        for key, value in card_data.items():
            if key.lower() != 'specialties':
                continue
            return value
        return 'no_info'

    @staticmethod
    def get_data_structure(card_path):
        card_info = card_path.find('dl', {'class': 'overflow-hidden'}).contents
        for each in card_info:  # del all non Tag data
            if isinstance(each, Tag):
                continue
            del card_info[card_info.index(each)]
        data = {}
        key = ''
        value = ''
        for each in card_info:
            if each.name == 'dt':
                if key:
                    if not value:
                        value = ''
                    data[key] = value
                    value = ''
                key = re.sub(r'\n', '', each.text).strip()
                continue
            elif each.name == 'dd':
                if value:
                    value = ', '.join([value, re.sub(r'\n', '', each.text).strip()])
                    continue
                value = re.sub(r'\n', '', each.text).strip()
                continue
        data[key] = value
        return data

    def get_card_info(self) -> Dict:
        card_path = self.src.find('section', {'class': 'artdeco-card p5 mb4'})
        card_data = self.get_data_structure(card_path)
        return {
            'title': self.get_title(),
            'overview': self.get_overview(card_path),
            'website': self.get_website(card_data),
            'phone': self.get_phone(card_data),
            'industry': self.get_industry(card_data),
            'company_size': self.get_company_size(card_data),
            'headquarters': self.get_headquarters(card_data),
            'founded': self.get_founded(card_data),
            'specialties': self.get_specialties(card_data),
            'location': self.get_location(),
            'followers': self.get_followers()
        }
