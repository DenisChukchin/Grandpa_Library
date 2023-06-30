import os
import argparse
import requests
from urllib.parse import urlparse, unquote, urljoin
from time import sleep
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename


def get_response_from_url(page_url):
    response = requests.get(page_url)
    response.raise_for_status()
    check_for_redirect(response.history)
    soup = BeautifulSoup(response.text, 'lxml')
    return soup


def parse_book_page(soup, page_url):
    title_tag = soup.find('head').find('title')
    book_title, author = title_tag.text.split(' - ')
    title = sanitize_filename(book_title)
    author = author.split(',')[0].strip()

    image_tag = soup.find(class_='bookimage').find('img')['src']
    picture_link = urljoin(page_url, image_tag)

    books_comments = soup.find_all(class_='texts')
    comments = [book_comment.find(class_='black').text
                for book_comment in books_comments]

    book_genre = soup.find_all('span', class_='d_book')
    genre = [book.text.split(': ')[1].replace('.', '').strip()
             for book in book_genre][0].split(', ')

    book_page = {
        'title': title,
        'author': author,
        'picture_link': picture_link,
        'comments': comments,
        'genre': genre
    }
    return book_page


def download_txt(number, url, filename, folder='books/'):
    os.makedirs("books", exist_ok=True)
    params = {
        'id': f'{number}'
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    check_for_redirect(response.history)
    with open(os.path.join(folder, f'{number}.{filename}.txt'), 'wb') as file:
        file.write(response.content)


def download_image(number, picture_link, folder='images/'):
    os.makedirs("images", exist_ok=True)
    if 'nopic.gif' not in picture_link:
        response = requests.get(picture_link)
        response.raise_for_status()
        check_for_redirect(response.history)
        picture_extension = get_extension_from_url(picture_link)
        with open(os.path.join(folder, f'{number}{picture_extension}'), 'wb') as file:
            file.write(response.content)


def get_extension_from_url(url):
    encode_link = unquote(url, encoding="utf-8", errors="replace")
    chopped_link = urlparse(encode_link)
    return os.path.splitext(chopped_link.path)[1]


def check_for_redirect(response_history):
    if response_history:
        raise requests.HTTPError


def parse_args():
    parser = argparse.ArgumentParser(
        description='Программа скачает книжки и обложки к ним. '
                    'На терминал выведется информация '
                    'с названиями книг, авторами, жанрами и отзывами. '
                    'Для работы программы потребуется указать'
                    ' интервал книг для загрузки. '
                    'По умолчанию скрипт скачает книги '
                    'в интервале с 1 по 10 включительно. '
    )
    parser.add_argument('start_id', type=int,
                        help='Номер книги с которой начнется загрузка. '
                             'Например: 15',
                        default=1, nargs='?',
                        metavar='Id книги - целое число.')
    parser.add_argument('end_id', type=int,
                        help='Номер книги после которой закончится загрузка. '
                             'Например: 35',
                        default=10, nargs='?',
                        metavar='Id книги - целое число.')
    args = parser.parse_args()
    return args.start_id, args.end_id + 1


def main():
    start_id, end_id = parse_args()
    url = 'https://tululu.org'
    txt_url = urljoin(url, 'txt.php')
    for number in range(start_id, end_id):
        try:
            page_url = urljoin(url, f'b{number}/')
            soup = get_response_from_url(page_url)
            book_page = parse_book_page(soup, page_url)
            download_image(number, book_page['picture_link'], folder='images/')
            download_txt(number, txt_url, book_page['title'], folder='books/')
            print(f"Книга: {book_page['title']}", f"\nАвтор: {book_page['author']}",
                  f"\nКомментарий: {book_page['comments']}", f"\nЖанр: {book_page['genre']}\n")
        except requests.HTTPError:
            print(f"Книга {number} отсутствует в каталоге\n")
        except requests.exceptions.ConnectionError as error:
            print(error, "Ошибка соединения")
            sleep(15)
        except requests.exceptions.ReadTimeout:
            print("Превышено время ожидания...")


if __name__ == "__main__":
    main()
