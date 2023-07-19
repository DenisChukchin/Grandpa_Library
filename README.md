# Grandpa Library
The first script is downloading book covers and books from [the website](https://tululu.org) as txt file and shows on the terminal authors, titles , genres and reviews.

The second script is downloading book covers and books from [category: Science fiction](https://tululu.org/l55/). Authors, titles, genres and reviews will be saved as a json file on your device.

The third script is needed to launch a website [Grandpa Library](https://denischukchin.github.io/Grandpa_Library/pages/index1.html) on localhost that simulates a library based on books that were downloaded earlier.
## Installation.
Install Python3 latest version. Install PyCharm IDE, if you need it.
> To isolate the project, I'd recommend to use a virtual environment model. [vertualenv/venv](https://docs.python.org/3/library/venv.html).
 ## Preparing to run the script.
+ Create a virtualenv and activate it.
+ Then use pip (or pip3, there is a conflict with Python2) to install the dependencies (use the requirements.txt file):
```bash
% pip install -r requirements.txt
```
## Run the scripts.
### parse_tululu.py
The following parameters are available for the script:
+ ```start_id``` - the first id book to download
+ ```end_id``` - the last id book to download
+ ```--dest_folder``` - path to download folder

User need to specify books interval by command:
```bash
% python3 parse_tululu.py 20 30
```
<img width="1392" alt="image" src="https://github.com/DenisChukchin/Grandpa_Library/assets/125466667/607cadc0-f8e9-4dd9-876b-243401a63e09">

### parse_tululu_category.py
The following parameters are available for the script:
+ ```--start_page``` - the first page to download
+ ```--end_page``` - the last page to download
+ ```--dest_folder``` - path to download folder
+ ```--skip_img``` - to skip downloading book covers
+ ```--skip_txt``` - to skip downloading books

One of the possible commands to use the script:
```bash
% python3 parse_tululu_category.py --start_page 700 --end_page
```
<img width="1045" alt="image" src="https://github.com/DenisChukchin/Grandpa_Library/assets/125466667/a128d822-7d0b-45a4-8dac-5c405a0f7cf7">

### render_website.py  
The script launches a simple website with books (even without internet connection). The site will display book titles, authors, genres and book covers. You can start reading the book by following the link 'Читать'.

The following parameter are available for the script:
+ ```--json_path``` - path to json file 

To launch website use this command:
```bash
% python3 render_website.py  
```
+ Then check your site: [localhost](http://127.0.0.1:5500)

> To see an example of what the site looks like, follow the link: [Grandpa Library](https://denischukchin.github.io/Grandpa_Library/pages/index1.html)

To launch a website without the Internet connection, you need to find a folder called __pages__ in the program directory. In this folder, you can run any html file and you get to the library.

<img width="1336" alt="image" src="https://github.com/DenisChukchin/Grandpa_Library/assets/125466667/ee4d8128-b410-40a4-8b00-3d5c1e7503b0">

## Project goals.
*The program was designed by a student from online web development courses for educational purposes [Devman](https://dvmn.org).*
