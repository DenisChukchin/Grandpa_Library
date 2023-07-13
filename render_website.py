import os
import json
from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server


def read_json_file(folder):
    with open(os.path.join(folder, 'BOOKS'), 'r') as json_file:
        books_json = json_file.read()
    books = json.loads(books_json)
    return books


def on_reload():
    book_descriptions = read_json_file(folder='books as json/')

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')
    rendered_page = template.render(
        book_descriptions=book_descriptions
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)


if __name__ == '__main__':
    on_reload()
    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='.')
