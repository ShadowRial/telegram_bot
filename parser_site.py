import requests
from bs4 import BeautifulSoup
import time
import sys
import json
from bot_telegram import *
from configs import *

sys.setrecursionlimit(1000000)  # Увеличение максимально возможного числа выполнения операций


class bucket():
    is_open = 'http://127.0.0.1:8000/containers/'  # Ссылка на сайт откуда будет браться информация
    # Указание моего user-agent (специального идентификатора пользователя) для того, чтобы можно было посещать сайты. Ищется в гугле по запросу my user agent
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}
    address = {}
    now = {}
    exepts = {}

    def get_opens(self):
        full_page = requests.get(self.is_open, headers=self.headers)  # Запрос полного html шаблона сайта
        # Здесь мы используем специальную библиотеку, которая будет выводить "более крректный" html шаблон
        soup = BeautifulSoup(full_page.content, 'html.parser')
        # Далее находим нужный html тег в котором содержатся нужные нам данные
        convert = soup.findAll("h4", {"class": "is_open"})
        return convert[0].text

    def get_address(self):
        full_page = requests.get(self.is_open, headers=self.headers)
        soup = BeautifulSoup(full_page.content, 'html.parser')
        addressed = soup.findAll("h3", {"class": "address"})
        return addressed[0].text

    def list_generator(self):
        for i, v in enumerate(self.get_opens().split()):
            self.now[i + 1] = v
            self.address[i + 1] = self.get_address()
    def check_change(self):
        if not self.now:  # Если список пуст, то запустить генерацию списка
            self.list_generator()
        if 'False' not in self.get_opens():
            self.exepts = {}  # Очищаем словарь
            print('Заполненных баков нет')
        else:
            print('Обнаружены закрытые баки')
            # Формируем список текущих значений
            for i, v in enumerate(self.get_opens().split()):
                # Если словарь пуст, то сразу создаём запись с полученным id
                if self.exepts == {}:
                    print(v, self.now.get(i + 1))
                    self.exepts[1] = v
                    print(self.exepts.keys())
                    print('Изменения: ', self.exepts, sep=' ')
                    self.send_mail()
                # Иначе сравниваем Flase с элементами полученного списка
                elif v == self.now.get(i + 1):
                    print(v, self.now.get(i + 1))
                    if i + 1 not in self.exepts:  # Если значение = False и его нет в списке, то создаём новую запись
                        self.exepts[i + 1] = v
                        print('Изменения: ', self.exepts)
                        self.send_mail()

        # Создаём словать исключений
        with open('exepts.json', 'w') as file:
            json.dump(self.exepts, file, indent=4, ensure_ascii=False)
        # Создаём словарь адрессов
        with open('address.json', 'w') as file:
            json.dump(self.address, file, indent=4, ensure_ascii=False)

        time.sleep(20)  # Время, через которое будет осуществляться повторная проверка данных на сайте
        self.check_change()

    def send_mail(self):
        # Здесь отправляется сообщение ботом в тг
        print('отправка сообщения')
        flag = ['True']

        with open('flag.json', 'w') as file:
            json.dump(flag, file, indent=4, ensure_ascii=False)


bucket = bucket()
bucket.check_change()
