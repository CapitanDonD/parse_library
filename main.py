import os
from pathlib import Path

from bs4 import BeautifulSoup
import requests


def finding_content(response):
    soup = BeautifulSoup(response.text, 'lxml')
    title_tag = soup.find(id="content").find('h1').text
    title_book, author_name = title_tag.split(' \xa0 :: \xa0 ')

    return title_book, author_name


def check_for_redirect(response):
    if response.history:
        raise requests.exceptions.HTTPError


def save_book(number_book, response):
    with open(f'books/book_{number_book}.txt', "w", encoding='UTF-8') as file:
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
            save_book(number_book, response)

            response = requests.get(page_book_url)
            title_book, author_name = finding_content(response)
            print(f'Заголовок: {title_book}\nАвтор: {author_name}')
        except requests.exceptions.HTTPError:
            print(f'Книги {number_book} не существует')


if __name__ == '__main__':
    main()
