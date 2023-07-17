import os
import json
from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked


def read_json_file(folder):
    with open(os.path.join(folder, 'BOOKS'), 'r') as json_file:
        books_json = json_file.read()
    books = json.loads(books_json)
    return books


def on_reload():
    os.makedirs('pages', exist_ok=True)
    book_descriptions = read_json_file(folder='books as json/')
    books_per_page = list(chunked(book_descriptions, 10))

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')

    for page_number, books in enumerate(books_per_page, 1):
        chunked_books = list(chunked(books, 2))
        rendered_page = template.render(
            chunked_books=chunked_books,
            current_page=page_number,
            total_pages=len(books_per_page)
        )
        with open(f'pages/index{page_number}.html', 'w', encoding="utf8") as file:
            file.write(rendered_page)


if __name__ == '__main__':
    on_reload()
    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='.', default_filename='pages/index1.html')
