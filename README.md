# Grandpa Library
The first script is downloading book covers and books from [the website](https://tululu.org) as txt file and shows on the terminal authors, titles , genres and reviews.

The second script is downloading book covers and books from [category: Science fiction](https://tululu.org/l55/). Authors, titles, genres and reviews will be saved as a json file on your device.
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
% python3 main.py 20 30
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


## Project goals.
*The program was designed by a student from online web development courses for educational purposes [Devman](https://dvmn.org).*
