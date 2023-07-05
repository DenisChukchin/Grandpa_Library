import os
import requests
import json
from urllib.parse import urljoin
from time import sleep
from main import get_response_from_url, parse_book_page, download_txt
from main import download_image


def get_id(url, page_url):
    id_tags = page_url.find('div', id='content').find_all(class_='d_book')
    ids_url = []
    for id_tag in id_tags:
        id_url = urljoin(url, id_tag.find('a')['href'])
        ids_url.append(id_url)
    return ids_url


def save_books_as_json_file(books_description, folder='books_as_json/'):
    os.makedirs("books_as_json", exist_ok=True)
    with open(os.path.join(folder, 'BOOKS'), 'w', encoding='utf8') as json_file:
        json.dump(books_description, json_file, ensure_ascii=False)


def main():
    url = 'https://tululu.org'
    txt_url = urljoin(url, 'txt.php')
    ids_url = []
    for page in range(1, 5):
        try:
            category_page_url = urljoin(url, f'l55/{page}')
            page_urls = get_response_from_url(category_page_url)
            ids_url.extend(get_id(url, page_urls))
        except requests.exceptions.ConnectionError as error:
            print(error, "Ошибка соединения")
            sleep(15)
        except requests.exceptions.ReadTimeout:
            print("Превышено время ожидания...")
    books_description = []
    for number, id_url in enumerate(ids_url):
        try:
            soup = get_response_from_url(id_url)
            book_page = parse_book_page(soup, id_url)
            image_path = (download_image(number, book_page['picture_link'], folder='images/')
                          if 'nopic.gif' not in book_page['picture_link']
                          else 'Обложки нет на сайте')
            txt_path = download_txt(number, txt_url, book_page['title'], folder='books/')
            books_description.append({
                'title': book_page['title'],
                'author': book_page['author'],
                'img_src': image_path,
                'book_path': txt_path,
                'comments': book_page['comments'],
                'genres': book_page['genre'],
            })
        except requests.HTTPError:
            print(f"Книга {number} отсутствует в каталоге")
        except requests.exceptions.ConnectionError as error:
            print(error, "Ошибка соединения")
            sleep(15)
        except requests.exceptions.ReadTimeout:
            print("Превышено время ожидания...")

    save_books_as_json_file(books_description, folder='books_as_json/')


if __name__ == "__main__":
    main()
