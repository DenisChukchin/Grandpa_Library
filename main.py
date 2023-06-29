import requests
import os
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename


def get_book_title(number):
    url = f'https://tululu.org/b{number}/'
    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response.history)
    soup = BeautifulSoup(response.text, 'lxml')
    title_tag = soup.find('head').find('title')
    book_title, author = title_tag.text.split(' - ')
    book_name = sanitize_filename(book_title)
    book_author = author.split(',')[0].strip()
    return book_name, book_author


def download_txt(number, filename, folder='books/'):
    os.makedirs("books", exist_ok=True)
    url = f"https://tululu.org/txt.php?id={number}"
    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response.history)
    with open(os.path.join(folder, f'{number}.{filename}.txt'), 'wb') as file:
        file.write(response.content)


def check_for_redirect(response_history):
    if response_history:
        raise requests.HTTPError


def main():
    for number in range(1, 11, 1):
        try:
            filename, author = get_book_title(number)
            download_txt(number, filename, folder='books/')
        except requests.HTTPError:
            print(f"Книги {number} нет в каталоге")


if __name__ == "__main__":
    main()
