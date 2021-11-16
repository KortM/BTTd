
import os
import subprocess
import requests
import bs4
from schedule import every, repeat, run_pending
import time
import datetime
import colorama
from colorama import Fore, Back, Style
import schedule
import json

class TronChecker:
    def __init__(self, btfs_password:str, btfs_path:str):
        '''
            Конструктор класса принимает как аргументы адрес локального кошелька и порт для подключения. 
            Пример: http://127.0.0.1:5000/api/status?tTWMVh5ZjSVNRM9y4DsgANf
        '''
        self.password = btfs_password
        self.path = btfs_path
        colorama.init()

    def get_balance(self) -> None:
        '''
            Метод проверяет баланс BTT-разработчика на сети tron, если баланс > 500000 BTT, то выводим.
            Метод не возвращает ничего, только консольный вывод. 
        '''
        
        print(datetime.datetime.now())
        try:
            result = requests.get('https://apilist.tronscan.org/api/account?address=TA1EHWb1PymZ1qpBNfNj9uTaxd18ubrC7a')
            amount_BTT = None
            amount_BTT_convert = None
            our_BTT = None
            our_BTT_convert = None
            for line in result.json()['tokenBalances']:
                if line['tokenName'] == 'BitTorrent':
                    print(Fore.YELLOW + 'Текущий баналс разработчика BTT: {}.{}'.format(line["balance"][:-int(line["tokenDecimal"])], line['balance'][-int(line["tokenDecimal"]):]))
                    amount_BTT_convert = float('{}.{}'.format(line["balance"][:-int(line["tokenDecimal"])], line['balance'][-int(line["tokenDecimal"]):]))
                    amount_BTT = int(line['balance'])
        except Exception as e:
            print('Ошибка при получении баланса на TRON', e)
        try:
            result = subprocess.check_output('{} wallet balance'.format(os.path.normpath(self.path+'\\btfs.exe')))
            our_BTT = json.loads(result.decode('utf-8'))['BtfsWalletBalance']
            print(Fore.GREEN + 'Баланс нашего кошелька: {} BTT'.format(our_BTT))
            
            if our_BTT > amount_BTT:
                print(Fore.RED + 'Наш баланс > чем баланс разработчика. Вывода не будет, ждем пополнения')
            else:
                if our_BTT > 1000:
                    print(Fore.GREEN + 'Баланс разработчика < чем наш баланс.\n Запускаем ввывод.')
                    res = subprocess.check_output('{} wallet withdraw {} -p {}'.format(os.path.normpath(self.path+'\\btfs.exe'), our_BTT, self.password))
                    #res = subprocess.check_output(f'{os.path.normpath(self.path+"\\btfs.exe")} wallet withdraw {our_BTT} -p {self.password}')
                    print(res.decode('utf-8'))
                else:
                    print(Fore.LIGHTRED_EX + 'На балансе меньше 1000 BTT')
        except Exception as e:
            print(Fore.RED + 'Не удалось подключиться к локальному кошельку! При повторном запуске проверьте адрес/порт. ',e)
        print(Style.RESET_ALL)

    def task(self):
        print('Запускаем скрипт ...')
        schedule.every(5).seconds.do(self.get_balance)
        while True:
            run_pending()
            time.sleep(1)
    
        

if __name__ == '__main__':
    path = input('Введите путь к BTFS.exe: ')
    key = input('Введите пароль от BTFS: ')
    t = TronChecker(key, path)
    t.task()