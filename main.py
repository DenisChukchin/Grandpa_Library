import requests
import os
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib.parse import urlparse, unquote, urljoin


def parsing_book_page(number):
    url = f'https://tululu.org/b{number}/'
    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response.history)
    soup = BeautifulSoup(response.text, 'lxml')

    title_tag = soup.find('head').find('title')
    book_title, author = title_tag.text.split(' - ')
    book_name = sanitize_filename(book_title)
    book_author = author.split(',')[0].strip()

    image_tag = soup.find(class_='bookimage').find('img')['src']
    picture_link = urljoin(url, image_tag)

    genre = []
    book_genre_info = soup.find_all('span', class_='d_book')
    for book in book_genre_info:
        book = book.text.split(': ')[1].replace('.', '').strip()
        genre.append(book.split(', '))

    books_comments = soup.find_all(class_='texts')
    if books_comments is not None:
        comments = [book_comment.find(class_='black').text
                    for book_comment in books_comments]
        return book_name, book_author, picture_link, comments, genre[0]


def download_txt(number, filename, folder='books/'):
    os.makedirs("books", exist_ok=True)
    url = f"https://tululu.org/txt.php?id={number}"
    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response.history)
    with open(os.path.join(folder, f'{number}.{filename}.txt'), 'wb') as file:
        file.write(response.content)


def download_image(number, picture_link, folder='images/'):
    os.makedirs("images", exist_ok=True)
    if 'nopic.gif' not in picture_link:
        response = requests.get(picture_link)
        response.raise_for_status()
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


def main():
    for number in range(1, 11, 1):
        try:
            filename, author, picture_link, comments, genre = parsing_book_page(number)
            download_image(number, picture_link, folder='images/')
            download_txt(number, filename, folder='books/')
        except requests.HTTPError:
            print(f"Книги {number} нет в каталоге")


if __name__ == "__main__":
    main()
