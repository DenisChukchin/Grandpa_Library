import requests
import os


def download_books():
    os.makedirs("books", exist_ok=True)
    for number in range(1, 11, 1):
        url = f"https://tululu.org/txt.php?id={number}"
        response = requests.get(url)
        response.raise_for_status()
        filename = f"book_{number}.txt"
        with open(f"books/{filename}", 'wb') as file:
            file.write(response.content)


if __name__ == "__main__":
    download_books()
