

import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from pprint import pprint
from get_redirect import check_for_redirect

def search_book_urls(start_page, end_page):
    books_urls = []

    for page in range(start_page, end_page):
        genre_url = f'https://tululu.org/l55/{page}'

        response = requests.get(genre_url)
        response.raise_for_status()
        check_for_redirect(response)

        soup = BeautifulSoup(response.text, 'lxml')

        books_id = soup.find_all('table', class_='d_book')

        for book_id in books_id:
            book_url = urljoin(f'https://tululu.org/l55/', book_id.find('a')['href'])
            books_urls.append(book_url)

    return books_urls


def main():
    pprint()


if __name__ == '__main__':
    main()
