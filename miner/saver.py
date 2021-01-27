import os
import time
import string
from bs4 import BeautifulSoup
from miner.config import config_data
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print(BASE_DIR)
def save(name, chapter_page, directory):
    # chapters = chapters[:2]
    filename = format_filename(f"{name}.txt")
    print(filename)
    filepath = os.path.join(directory, filename)
    data = chapter_page.find('div', class_='chapter-content')
    text = clean([i.get_text() for i in data.select('p')])
    with open(filepath, 'w') as f:
        for line in text:
            f.write(line + '\n')
    # print(text[:5], text[-5:])
    print("Created:", filename)

def format_filename(s):
    """
    Take a string and return a valid filename constructed from the string.
    Uses a whitelist approach: any characters not present in valid_chars are
    removed. Also spaces are replaced with underscores.
    
    Note: this method may produce invalid filenames such as ``, `.` or `..`
    """
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    filename = ''.join(c for c in s if c in valid_chars)
    # filename = filename.replace(' ','_') 
    return filename

def clean(text):
    res = []
    exclude = config_data["Text"]["exclude"].split(',')
    # print(exclude)
    for line in text:
        if not line in exclude:
            res.append(line)
    if res[0] != '':
        res[0] = "# " + res[0]
    else:
        res[1] = "# " + res[1]
        res = res[1:]
    return res