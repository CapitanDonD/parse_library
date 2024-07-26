import os
import argparse
from pathlib import Path
from time import sleep
import json

import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib.parse import urljoin, urlsplit, urlparse

from parse_tululu_category import search_book_urls
from get_redirect import check_for_redirect
from render_website import get_cards_content


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


def download_txt(response, book_filename, folder):
    book_filename = sanitize_filename(book_filename)
    filename = f'{book_filename}.txt'
    path = os.path.join(folder, filename)

    with open(path, 'w', encoding='UTF-8') as file:
        file.write(response.text)


def download_image(image_url, image_name, folder):
    response = requests.get(image_url)
    response.raise_for_status()
    path = os.path.join(folder, image_name)

    with open(path, 'wb') as file:
        file.write(response.content)


def main():
    arg = argparse.ArgumentParser(
        description=' To start downloading from a specific book add argument --start_page, to finish on a specific book\
             add argument --end_page'
    )

    arg.add_argument('--start_page', default=1, type=int, help='start downloading from a specific book')
    arg.add_argument('--end_page', default=11, type=int, help='finish on a specific book')
    arg.add_argument('--dest_folder', default='parse_library_content', type=str, help='folder which in saves images and texts')
    arg.add_argument('--skip_imgs', action='store_true',  help='download images or dont')
    arg.add_argument('--skip_txt', action='store_true', help='download texts or not')
    arg.add_argument(
        '--json_path',
        default='parse_library_content',
        help='show path to the json file with results'
    )

    args = arg.parse_args()
    start_page = args.start_page
    end_page = args.end_page
    dest_folder = args.dest_folder
    skip_imgs = args.skip_imgs
    skip_txt = args.skip_txt
    books_content = []
    image_folder = f'{dest_folder}/image'
    books_folder = f'{dest_folder}/books'
    json_folder = f'{args.json_path}/'

    book_urls = search_book_urls(start_page, end_page)

    for book_url in book_urls:
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
            numbered_book_title = f'{book_params["book_title"]}'
            if not skip_txt:
                Path(books_folder).mkdir(parents=True, exist_ok=True)
                download_txt(book_response, numbered_book_title, books_folder)
            if not skip_imgs:
                Path(image_folder).mkdir(parents=True, exist_ok=True)
                download_image(
                    book_params['book_image_url'],
                    book_params['image_name'],
                    image_folder
                )
            books_content.append(book_params)

        except requests.exceptions.HTTPError:
            print(f'Книги {book_number} не существует')
        except requests.ConnectionError:
            print('Не удалось восстановить соединение')
            sleep(20)

    Path(json_folder).mkdir(parents=True, exist_ok=True)

    with open(f'{json_folder}json_books_content.json', 'w', encoding="utf-8") as file:
        json.dump(books_content, file, ensure_ascii=False)


if __name__ == '__main__':
    main()
