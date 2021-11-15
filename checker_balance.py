import requests
import bs4
from schedule import every, repeat, run_pending
import time
import datetime
import colorama
from colorama import Fore, Back, Style
import schedule

class TronChecker:
    def __init__(self, cash_key=str, port=str):
        '''
            Конструктор класса принимает как аргументы адрес локального кошелька и порт для подключения. 
            Пример: http://127.0.0.1:5000/api/status?tTWMVh5ZjSVNRM9y4DsgANf
        '''
        self.cash_key = cash_key
        self.port = port
        colorama.init()

    def get_balance(self) -> None:
        '''
            Метод проверяет баланс BTT-разработчика на сети tron, если баланс > 500000 BTT, то выводим.
            Метод не возвращает ничего, только консольный вывод. 
        '''
        print(datetime.datetime.now())
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
        try:
            result = requests.get('http://127.0.0.1:{}/api/status?t={}'.format(self.port,self.cash_key))
            our_BTT_convert = int(result.json()['balance'])/1000000
            our_BTT = int(result.json()['balance'])
            print(Fore.GREEN + 'Баланс нашего кошелька: {} BTT'.format(our_BTT_convert))
            
            '''
                Необходимо поменять алгоритм вывода из локального кошелька на chain.
                Торрент блокирует вывод через web-api             
            '''

            if our_BTT > amount_BTT:
                print(Fore.RED + 'Наш баланс > чем баланс разработчика. Вывода не будет, ждем пополнения')
            else:
                if our_BTT_convert > 1000:
                    print(Fore.GREEN + 'Баланс разработчика > чем наш баланс.\n Запускаем ввывод.')
                    result = requests.post('http://127.0.0.1:{}/api/exchange/withdrawal?t={}&amount={}'.format(self.port, self.cash_key, our_BTT))
                    if result.status_code == 200:
                        result = requests.get('http://127.0.0.1:{}/api/status?t={}'.format(self.port, self.cash_key))
                        our_BTT_convert = int(result.json()['balance'])/1000000
                        print('Запрос на вывод размещен\n Наш текущий баланс: {}'.format(our_BTT_convert))
                    else:
                        print(Fore.RED + 'Что-то пошло не так! Возможно нет средств на балансе.')
                else:
                    print(Fore.LIGHTRED_EX + 'На балансе меньше 1000 BTT')
        except Exception:
            print(Fore.RED + 'Не удалось подключиться к локальному кошельку! При повторном запуске проверьте адрес/порт. ')
        print(Style.RESET_ALL)

    def task(self):
        print('Запускаем скрипт ...')
        schedule.every(5).seconds.do(self.get_balance)
        while True:
            run_pending()
            time.sleep(1)
    
        

if __name__ == '__main__':
    key = input('Введите адрес кошёлька: ')
    port = input('Введите порт: ')
    t = TronChecker(key, port)
    t.task()