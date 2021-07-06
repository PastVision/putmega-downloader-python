import requests
from bs4 import BeautifulSoup
import os
from sys import argv
from tqdm import tqdm
from math import ceil


class PutMega:
    HEADER = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"}

    def __init__(self, url: str) -> None:
        self.url = url
        self.soup = BeautifulSoup(
            requests.get(url,
                         headers=self.HEADER).content.decode(),
            'html5lib'
        )

    def download(self):
        links = [i['href'] for i in self.soup.find_all(
            'a', {'class': 'image-container --media'})]
        pages = ceil(int(self.soup.find(
            'b', {'data-text': 'image-count'}).text)/len(links))
        nexturl = self.soup.find('a', {'data-pagination': 'next'})['href']
        for _ in range(pages-1):
            cont = requests.get(nexturl, headers=self.HEADER).content.decode()
            sp = BeautifulSoup(cont, 'html5lib')
            links += [i['href'] for i in sp.find_all(
                'a', {'class': 'image-container --media'})]
            try:
                nexturl = sp.find('a', {'data-pagination': 'next'})['href']
            except:
                break
        self.folder = './'+self.url.split('/')[-1]
        if not os.path.exists(self.folder):
            os.mkdir(self.folder)
        print('Downloading...')
        for i in tqdm(links):
            self.__download(i)

    def __download(self, link: str):
        cntnt = requests.get(link, headers=self.HEADER).content.decode()
        soup = BeautifulSoup(cntnt, 'html5lib')
        url = soup.find('a', {'class': 'btn btn-download default'})['href']
        name = url.split('/')[-1]
        try:
            img = requests.get(url, headers=self.HEADER)
            with open(self.folder + '/' + name, 'wb') as f:
                for chunk in img:
                    f.write(chunk)
        except Exception as e:
            print('Error:', e)


if __name__ == '__main__':
    if len(argv) > 1:
        x = PutMega(argv[1])
        x.download()
    else:
        print('No URL Passed')
