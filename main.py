import os
import argparse
from pathlib import Path
from time import sleep

import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib.parse import urljoin, urlsplit, urlparse

from parse_tululu_category import search_book_url


def parse_book_page(response, book_page_url):
    soup = BeautifulSoup(response.text, 'lxml')

    title_tag = soup.select_one('h1').text
    book_title, author_name = title_tag.split(' \xa0 :: \xa0 ')

    image_path = soup.select_one('div.bookimage img')['src']
    book_image_url = urljoin(book_page_url, image_path)
    image_name = urlsplit(book_image_url).path.split('/')[-1]

    book_comments = soup.select('div.texts')
    book_comments_text = '\n'.join([comment.select_one('span.black').text for comment in book_comments])

    book_genres = soup.select_one('span.d_book').select('a')
    book_genres_text = [genre.text for genre in book_genres]

    picture_params = {
        'author_name': author_name,
        'book_title': book_title,
        'book_image_url': book_image_url,
        'image_name': image_name,
        'comments': book_comments_text,
        'genres': book_genres_text
    }

    return picture_params


def check_for_redirect(response):
    if response.history:
        raise requests.exceptions.HTTPError


def download_txt(response, book_filename, folder='books/'):
    book_filename = sanitize_filename(book_filename)
    filename = f'{book_filename}.txt'
    path = os.path.join(folder, filename)

    with open(path, "w", encoding='UTF-8') as file:
        file.write(response.text)


def download_image(image_url, image_name, folder):
    response = requests.get(image_url)
    response.raise_for_status()
    path = os.path.join(folder, image_name)

    with open(path, "wb") as file:
        file.write(response.content)


def main():
    arg = argparse.ArgumentParser(
        description=' To start downloading from a specific book add argument --start_id, to finish on a specific book\
             add argument --end id'
    )

    arg.add_argument('--start_id', default=1, type=int, help='start downloading from a specific book')
    arg.add_argument('--end_id', default=11, type=int, help='finish on a specific book')

    args = arg.parse_args()
    start_id = args.start_id
    end_id = args.end_id
    books_folder_name = 'books'
    image_folder_name = 'image'

    Path(image_folder_name).mkdir(parents=True, exist_ok=True)
    Path(books_folder_name).mkdir(parents=True, exist_ok=True)

    books_url = search_book_url()

    for book_url in books_url:
        book_number = urlparse(book_url).path.split('/')[1][1:]
        params = {'id': book_number}
        book_txt_url = 'https://tululu.org/txt.php'
        try:
            book_response = requests.get(book_txt_url, params=params)
            book_response.raise_for_status()
            check_for_redirect(book_response)

            response = requests.get(book_url)
            response.raise_for_status()
            check_for_redirect(response)
            book_params = parse_book_page(response, book_url)
            numbered_book_title = f'{book_number}.{book_params["book_title"]}'
            download_txt(book_response, numbered_book_title)
            download_image(book_params['book_image_url'], book_params['image_name'], image_folder_name)

        except requests.exceptions.HTTPError:
            print(f'Книги {book_number} не существует')
        except requests.ConnectionError:
            print('Не удалось восстановить соединение')
            sleep(20)


if __name__ == '__main__':
    main()
