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
    for cards_index, cards in enumerate(cards_content, 1, 2):
        pprint(cards)
        page_index_name = 1

        if cards_index > 10:
            page_index_name+=1

        chuncked_cards_content = list(chunked(cards, 2))

        env = Environment(
            loader=FileSystemLoader('.')
        )
        template = env.get_template('template.html')

        rendered_page = template.render(
            chuncked_cards_content = chuncked_cards_content,
            cards_content = cards
        )

        with open(f'pages/index{page_index_name}.html', 'w', encoding="utf8") as file:
            file.write(rendered_page)


def main():
    os.makedirs('pages', exist_ok=True)
    on_reload()
    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='.')



if __name__ == '__main__':
    main()
