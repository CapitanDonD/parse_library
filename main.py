import os
from pathlib import Path

import requests


def check_for_redirect(response):
    if response.history:
        raise requests.exceptions.HTTPError


def save_book(number_book, response):
    with open(f'books/book_{number_book}.txt', "w", encoding='UTF-8') as file:
        file.write(response.text)


def main():
    Path("books").mkdir(parents=True, exist_ok=True)

    for number_book in range(1, 11):
        params = {'id': number_book}
        book_txt_url = 'https://tululu.org/txt.php'
        response = requests.get(book_txt_url, params=params)
        try:
            response.raise_for_status()
            check_for_redirect(response)

            save_book(number_book, response)
        except requests.exceptions.HTTPError:
            print(f'Книги {number_book} не существует')


if __name__ == '__main__':
    main()
