import requests
from bs4 import BeautifulSoup
import time

import json
from bot_telegram import *
from configs import *
import sys

sys.setrecursionlimit(1000000)  # Увеличение максимально возможного числа выполнения операций


class bucket():
    is_open = 'http://127.0.0.1:8000/containers/'  # Ссылка на сайт откуда будет браться информация
    # Указание моего user-agent (специального идентификатора пользователя) для того, чтобы можно было посещать сайты. Ищется в гугле по запросу my user agent
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}
    now = []
    fulled = []

    def containers_generation(self):
        full_page = requests.get(self.is_open, headers=self.headers)  # Запрос полного html шаблона сайта
        # Здесь мы используем специальную библиотеку, которая будет выводить "более крректный" html шаблон
        soup = BeautifulSoup(full_page.content, 'html.parser')
        # Далее находим нужный html тег в котором содержатся нужные нам данные
        full = soup.findAll("h4", {"class": "is_open"})
        addressed = soup.findAll("h3", {"class": "address"})
        # Пробегаем в радиусе длины списка контейнеров и добавяем значения в словарь
        for i in range(len(full)):
            self.now.append([i + 1, addressed[i].text, full[i].text[0:6]])
        with open('containers_now.json', 'w') as file:
            json.dump(self.now, file, indent=4, ensure_ascii=False)
        with open('address.json', 'w') as file:
            json.dump(self.now, file, indent=4, ensure_ascii=False)
            self.send_mail()
        self.check_close()

    def check_close(self):
        for v in self.now:
            if v[2] == 'Закрыт':
                if v not in self.fulled:
                    self.fulled.append(v)

                    with open('exepts.json', 'w') as file:
                        json.dump(self.fulled, file, indent=4, ensure_ascii=False)
                        self.send_mail()
            else:
                if v in self.fulled:
                    self.fulled.remove(v)
        print(self.now)
        time.sleep(6)  # Засыпание на n секунд
        self.now.clear()
        self.containers_generation()

    def send_mail(self):
        flag = 'True'
        with open('flag.json', 'w') as file:
            json.dump(flag, file, indent=4, ensure_ascii=False)


bucket = bucket()
bucket.containers_generation()
