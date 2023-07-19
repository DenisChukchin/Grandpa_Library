import os
import json
import argparse
from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked


def read_json_file(folder):
    with open(folder, encoding='utf8') as json_file:
        books_json = json.load(json_file)
    return books_json


def parse_args():
    parser = argparse.ArgumentParser(
        description='Программа запускает простой сайт с книжками. '
                    'На сайте будут отображены названия книг, авторы, '
                    'жанр и обложки книг. Пройдя по ссылке "читать" - '
                    'откроется книга в новой вкладке. '
    )
    parser.add_argument('--json_path', type=str,
                        default='books as json/BOOKS',
                        help='Введите путь до файла json, в котором '
                             'хранится информация о скаченных книгах. '
                             'По умолчанию json файл находится в папке '
                             'с программой.',
                        metavar='Путь до файла json.')
    args = parser.parse_args()
    return args.json_path


def on_reload():
    os.makedirs('pages', exist_ok=True)
    json_path = parse_args()

    book_descriptions = read_json_file(folder=json_path)
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
