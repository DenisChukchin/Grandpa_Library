import os
import json
from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape


def read_json_file(folder):
    with open(os.path.join(folder, 'BOOKS'), 'r') as json_file:
        books_json = json_file.read()
    books = json.loads(books_json)
    return books


def main():
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

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
