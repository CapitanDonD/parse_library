# Parse library
This programme is created for download books from the library.
### Online pages on git hub
https://capitandond.github.io/parse_library/pages/index1.html - url for main page of the site
### How to install
Python3 should be already installed.
Then use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:
```
pip install -r requirements.txt
```
### How to run
To run the program itself, you need to write the following command on the command line:
```
python main.py 
```

If you want to download books pages in a certain range, then when calling, add commands when calling as shown in the example:
```
python main.py --start_page *page from* --end_page *page to*
```

If you want to download all parsing results:
```
python main.py --dest_folder *folder in which you want*
```
in addiction, if folder which you indicates, doesn't exist, it will be create

If you want to skip text download and/or image download:
```
python main.py --skip_imgs
```
or
```
python main.py --skip_txt
```
If you want to specify a different path to download the .json file:
```
python main.py --json_path *folder in which you want*
```
### How to run site with books
To run the site with all books, write in cmd
```
python render_website.py
```

### How to run the site offline
Before start it offline, you need to download books it in the step above

All downloaded pages of the site are stored in the folder `/parse_library/pages/`
Then you just need to double-click on any of the downloaded files to make the site work offline.
