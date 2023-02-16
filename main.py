import os
import argparse
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib.parse import urljoin, urlsplit


def parse_book_page(response):
    soup = BeautifulSoup(response.text, 'lxml')
    title_tag = soup.find(id="content").find('h1').text
    title_book, author_name = title_tag.split(' \xa0 :: \xa0 ')
    image_path = soup.find('div', class_='bookimage').find('img')['src']
    book_image_url = urljoin('https://tululu.org', image_path)
    image_name = urlsplit(book_image_url).path.split('/')[-1]
    book_comments = soup.find(id="content").find_all('div', class_='texts')
    book_comments_text = '\n'.join([comment.find('span', class_='black').text for comment in book_comments])
    book_genres = soup.find(id="content").find('span', class_='d_book').find_all('a')
    book_genres_text = [genre.text for genre in book_genres]
    picture_params = {
        'author_name': author_name,
        'title_book': title_book,
        'book_image_url': book_image_url,
        'image_name': image_name,
        'comments': book_comments_text,
        'genre': book_genres_text
    }

    return picture_params


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


def download_image(book_params, folder):
    image_url = book_params['book_image_url']
    image_name = book_params['image_name']
    response = requests.get(image_url)
    response.raise_for_status()
    path = os.path.join(folder, image_name)

    with open(path, "wb") as file:
        file.write(response.content)


def main():
    arg = argparse.ArgumentParser()
    arg.add_argument('--start_id', default=1, type=int)
    arg.add_argument('--end_id', default=11, type=int)
    args = arg.parse_args()
    start_id = args.start_id
    end_id = args.end_id
    name_books_folder = 'books'
    name_image_folder = 'image'
    Path(name_image_folder).mkdir(parents=True, exist_ok=True)
    Path(name_books_folder).mkdir(parents=True, exist_ok=True)
    for number_book in range(start_id, end_id):
        page_book_url = f'https://tululu.org/b{number_book}/'
        params = {'id': number_book}
        book_txt_url = 'https://tululu.org/txt.php'
        response = requests.get(book_txt_url, params=params)
        try:
            response.raise_for_status()
            check_for_redirect(response)

            response = requests.get(page_book_url)
            book_params = parse_book_page(response)
            numbered_title_book = f'{number_book}.{book_params["title_book"]}'
            download_txt(page_book_url, numbered_title_book)
            download_image(book_params, name_image_folder)

        except requests.exceptions.HTTPError:
            print(f'Книги {number_book} не существует')


if __name__ == '__main__':
    main()
