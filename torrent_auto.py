import requests
import bs4

class TorrentLoader:
    '''Загружаем данные с RarBG.org'''
    proxy_defalut = {
        'http':'socks4://162.247.18.162:4153'
    }
    def __init__(self, url, min_size) -> None:
        self.url = url
        self.min_size = min_size

    def start(self):
        session = requests.Session()
        session.proxies = self.proxy_defalut
        result = session.get(self.url)
        
        
        soup = bs4.BeautifulSoup(result.text, 'html.parser')
        data = soup.find_all('table', class_ = 'lista2t')
        print(data)


if __name__ == '__main__':
    t = TorrentLoader('https://rarbgmirror.org/torrents.php?r=55589966', 200)
    t.start()