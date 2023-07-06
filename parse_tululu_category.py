import os
import requests
import json
import argparse
from urllib.parse import urljoin
from time import sleep
from parse_tululu import parse_book_page, get_response_from_url
from parse_tululu import download_image, download_txt


def get_id(url, page_url):
    id_tags = page_url.select('.d_book .bookimage a')
    ids_url = [urljoin(url, id_tag['href']) for id_tag in id_tags]
    return ids_url


def save_books_as_json_file(books_description, folder):
    os.makedirs(folder, exist_ok=True)
    with open(os.path.join(folder, 'BOOKS'), 'w', encoding='utf8') as json_file:
        json.dump(books_description, json_file, ensure_ascii=False)


def parse_args():
    parser = argparse.ArgumentParser(
        description='Программа скачает книжки и обложки к ним. '
                    'На компьютер будет скачан текстовый файл '
                    'с названиями книг, авторами, жанрами и отзывами. '
                    'Для работы программы потребуется указать'
                    ' интервал страниц сайта с книгами для загрузки. '
                    'По умолчанию скрипт скачает книги со страницы 1. '
                    'По желанию можно указать папку для скачивания. '
                    'Также можно уточнить скачивать или нет книги'
                    ' и обложки к ним. '
    )
    parser.add_argument('--start_page', type=int,
                        help='Номер книги с которой начнется загрузка.',
                        metavar='Id книги - целое число.')
    parser.add_argument('--end_page', type=int,
                        help='Номер книги после которой закончится загрузка. '
                             'Если не указать этот параметр, то скачаются ВСЕ '
                             'книги начиная с паметра start_page до конца категории.',
                        metavar='Id книги - целое число.')
    parser.add_argument('--dest_folder', type=str, default=os.getcwd(),
                        help='Путь до папки для сохранения книг, обложек '
                             'и описания книжек. По умолчанию '
                             'все скачается в папку со скриптом.',
                        metavar='Путь до папки')
    parser.add_argument('--skip_img', action='store_true',
                        help='Скачиваем или не скачиваем обложки книг. '
                             'Не скачиваем: --skip_img, '
                             'Скачиваем: параметр отсутствует.')
    parser.add_argument('--skip_txt', action='store_true',
                        help='Скачиваем или не скачиваем книги. '
                             'Не скачиваем: --skip_txt, '
                             'Скачиваем: параметр отсутствует.')
    args = parser.parse_args()
    if not args.start_page and not args.end_page:
        return 1, 2, args.dest_folder, args.skip_img, args.skip_txt
    else:
        return args.start_page, args.end_page, args.dest_folder, args.skip_img, args.skip_txt


def main():
    url = 'https://tululu.org'
    science_fiction = 'https://tululu.org/l55/'
    txt_url = urljoin(url, 'txt.php')

    start_page, end_page, user_folder, skip_img, skip_txt = parse_args()
    ids_url = []
    try:
        start_page_url = urljoin(science_fiction, f'{start_page}')
        soup = get_response_from_url(start_page_url)
        last_page = [(int(soup.select('.npage')[-1].text) + 1)
                     if end_page is None else end_page][0]
        for page in range(start_page, last_page):
            category_page_url = urljoin(science_fiction, f'{page}')
            soup = get_response_from_url(category_page_url)
            ids_url.extend(get_id(url, soup))
    except requests.exceptions.ConnectionError as error:
        print(error, "Ошибка соединения")
        sleep(15)
    except requests.exceptions.ReadTimeout:
        print("Превышено время ожидания...")

    books_description = []
    for id_url in ids_url:
        id_number = id_url.split('b')[1].split('/')[0]
        try:
            soup = get_response_from_url(id_url)
            book_page = parse_book_page(soup, id_url)
            if not skip_img:
                image_path = (download_image(id_number, book_page['picture_link'],
                              folder=f'{user_folder}/images/')
                              if 'nopic.gif' not in book_page['picture_link']
                              else 'Обложки нет на сайте')
            else:
                image_path = 'Вы отменили скачивание обложек книг'
            if not skip_txt:
                txt_path = download_txt(id_number, txt_url, book_page['title'],
                                        folder=f'{user_folder}/books/')
            else:
                txt_path = 'Вы отменили скачивание книг'
            books_description.append({
                'title': book_page['title'],
                'author': book_page['author'],
                'img_src': image_path,
                'book_path': txt_path,
                'comments': book_page['comments'],
                'genres': book_page['genre'],
            })
            print(f"Книга {id_number}: {book_page['title']}",
                  f"Автор: {book_page['author']}")
        except requests.HTTPError:
            print(f"Книга {id_number} отсутствует в каталоге")
        except requests.exceptions.ConnectionError as error:
            print(error, "Ошибка соединения")
            sleep(15)
        except requests.exceptions.ReadTimeout:
            print("Превышено время ожидания...")

    save_books_as_json_file(books_description,
                            folder=f'{user_folder}/books as json/')
    print(f'Всего скачано книг: {len(books_description)}')


if __name__ == "__main__":
    main()
