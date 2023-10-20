import json
import os

from livereload import Server
from pprint import pprint
from jinja2 import Environment, FileSystemLoader
from more_itertools import chunked


def get_cards_content():
    with open("parse_library_content/json_books_content.json", "r", encoding="utf-8") as file:
        books_content = json.load(file)

    return books_content


def on_reload():
    cards_content = get_cards_content()
    pages = list(chunked(cards_content, 10))
    for page_index, pages in enumerate(pages, 1):
        chuncked_pages = list(chunked(pages, 2))

        env = Environment(
            loader=FileSystemLoader('.')
        )
        template = env.get_template('template.html')

        rendered_page = template.render(
            chuncked_pages=chuncked_pages,
            page_indexes=page_index
        )
        print(rendered_page)

        with open(f'pages/index{page_index}.html', 'w', encoding="utf8") as file:
            file.write(rendered_page)


def main():
    os.makedirs('pages', exist_ok=True)
    on_reload()
    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='.')



if __name__ == '__main__':
    main()
