

import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from pprint import pprint


def search_book_url():
    books_urls = []

    for page in range(0, 11):
        url_genre = f'https://tululu.org/l55/{page}'

        response = requests.get(url_genre)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'lxml')

        books_id = soup.find_all('table', class_='d_book')

        for book_id in books_id:
            book_url = urljoin(f'https://tululu.org/', book_id.find('a')['href'])
            books_urls.append(book_url)

    return books_urls


def main():
    pprint(search_book_url())


if __name__ == '__main__':
    main()
