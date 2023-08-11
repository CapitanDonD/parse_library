import json

from livereload import Server
from jinja2 import Environment, FileSystemLoader
from more_itertools import chunked


def get_cards_content():
    with open("parse_library/json_books_content.json", "r", encoding="utf-8") as file:
        books = json.load(file)

    return books


def on_reload():
    cards_content = get_cards_content()

    chuncked_cards_content = list(chunked(cards_content, 2))

    env = Environment(
        loader=FileSystemLoader('.')
    )
    template = env.get_template('template.html')

    rendered_page = template.render(
        chuncked_cards_content = chuncked_cards_content,
        cards_content = cards_content
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)


def main():
    on_reload()
    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='.')


if __name__ == '__main__':
    main()
