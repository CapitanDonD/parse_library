import json
import os

from livereload import Server
from jinja2 import Environment, FileSystemLoader
from more_itertools import chunked
from math import ceil


def get_cards_content():
    with open("media/json_books_content.json", "r", encoding="utf-8") as file:
        books_content = json.load(file)

    return books_content


def on_reload():
    cards_content = get_cards_content()
    nuber_of_book_on_page = 10
    pages = list(chunked(cards_content, nuber_of_book_on_page))
    all_page_indexes = len(pages)
    number_of_columns = 2
    for page_index, pages in enumerate(pages, 1):
        chuncked_page = list(chunked(pages, number_of_columns))

        env = Environment(
            loader=FileSystemLoader('.')
        )
        template = env.get_template('template.html')

        rendered_page = template.render(
            chuncked_pages=chuncked_page,
            page_indexes=all_page_indexes,
            current_page=page_index,
            pages_quantity=all_page_indexes
        )

        with open(f'pages/index{page_index}.html', 'w', encoding="utf8") as file:
            file.write(rendered_page)


def main():
    os.makedirs('pages', exist_ok=True)
    on_reload()
    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='.', default_filename='pages/index1.html')



if __name__ == '__main__':
    main()
