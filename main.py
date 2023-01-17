import os
from pathlib import Path

from bs4 import BeautifulSoup
import requests
from pathvalidate import sanitize_filename


def finding_content(response):
    soup = BeautifulSoup(response.text, 'lxml')
    title_tag = soup.find(id="content").find('h1').text
    title_book, author_name = title_tag.split(' \xa0 :: \xa0 ')

    return title_book, author_name


def check_for_redirect(response):
    if response.history:
        raise requests.exceptions.HTTPError


def download_txt(url, book_filename, folder='books/'):
    response = requests.get(url)
    response.raise_for_status()
    book_filename = sanitize_filename(book_filename)
    filename = f'{book_filename}.txt'
    path = os.path.join(folder, filename)
    with open(path, "w", encoding='UTF-8') as file:
        file.write(response.text)


def main():
    Path("books").mkdir(parents=True, exist_ok=True)
    for number_book in range(1, 11):
        page_book_url = f'https://tululu.org/b{number_book}/'
        params = {'id': number_book}
        book_txt_url = 'https://tululu.org/txt.php'
        response = requests.get(book_txt_url, params=params)
        try:
            response.raise_for_status()
            check_for_redirect(response)

            response = requests.get(page_book_url)
            title_book, author_name = finding_content(response)
            numbered_title_book = f'{number_book}.{title_book}'
            download_txt(page_book_url, numbered_title_book)

        except requests.exceptions.HTTPError:
            print(f'Книги {number_book} не существует')


if __name__ == '__main__':
    main()
