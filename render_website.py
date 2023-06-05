import os

from jinja2 import Environment, FileSystemLoader, select_autoescape


def cards_content(image_folder, image_name, author_name, book_title):
    path = os.path.join(image_folder, image_name)
    content = {
        'author_name': author_name,
        'book_title': book_title,
        'image_path': path
    }

    return content


def template_render():
    env = Environment(
        loader=FileSystemLoader('.')
    )
    template = env.get_template('template.html')
