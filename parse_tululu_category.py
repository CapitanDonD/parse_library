from time import sleep

import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from get_redirect import check_for_redirect

def search_book_urls(start_page, end_page):
    books_urls = []

    try:
        for page in range(start_page, end_page):
            genre_url = f'https://tululu.org/l55/{page}'

            response = requests.get(genre_url)
            response.raise_for_status()
            check_for_redirect(response)

            soup = BeautifulSoup(response.text, 'lxml')

            book_ids = soup.find_all('table', class_='d_book')

            for book_id in book_ids:
                book_url = urljoin(f'https://tululu.org/l55/', book_id.find('a')['href'])
                books_urls.append(book_url)

    except requests.exceptions.HTTPError:
        print(f'Страницы не существует')

    except requests.ConnectionError:
        print('Не удалось восстановить соединение')
        sleep(20)

    return books_urls
