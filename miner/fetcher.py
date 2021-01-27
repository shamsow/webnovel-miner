import os
import time
import requests
from miner.saver import save
from miner.config import config_data
from bs4 import BeautifulSoup
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR = config_data.get("System", "data_dir")
URL = config_data.get("Website", "tbate_url")
BASE_URL = config_data.get("Website", "base_url")

headers = requests.utils.default_headers()
headers.update({
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
})

class Novel:
    chapters = []
    indices = {}
    def __init__(self, title):
        url = self._resolve_title(title)
        if url is not None:
            self.link = url
        # self.link = url
        self.base_url = BASE_URL
        page = requests.get(url, headers= headers)
        self.soup = BeautifulSoup(page.content, 'html.parser')
        # print(soup.prettify())
        self.title = self.soup.find('div', class_='novel-info').h1.get_text()
        print(f"Initialized {self.title} novel. Ready to mine...")

    def _resolve_title(self, title):
        """
        Attempt to the get the URL for the novel based on user input
        """
        try:
            return config_data.get("Website", title)
        except Exception as e:
            print("Title URL not configured")
            raise e

    def _create_folders(self):
        """
        Create the directories for the chapter storage if it doesn't exist
        """
        if not os.path.exists(os.path.join(BASE_DIR, DIR)):
            os.mkdir(os.path.join(BASE_DIR, DIR))
        directory = os.path.join(BASE_DIR, DIR, self.title)
        if not os.path.exists(directory):
            os.mkdir(directory)
        return directory

    def _get_chapters(self):
        """
        Fetch the chapters from the website
        """
        # Get all the chapter links from novel page and put links in a list
        content = self.soup.find_all('div', class_='chapter-list')
        chapters = [(i.get_text(), i['href']) for i in content[-1].select('div.list div.item a')]
        chapters.reverse()
        for (i, ch) in enumerate(chapters):
            self.indices[ch[0]] = i
        
        self.chapters = chapters
        return chapters
    def _get_latest_chapter(self, directory):
        """
        If any saved chapters exist, find the index of the latest chapter
        """
        files = os.listdir(directory)
        if files:
            print("Last saved chapter: ", files[-1])
            last_chapter = files[-1][:-4]
            return self.indices.get(last_chapter, -1)
        return -1
    
    def save_chapters(self, count=-1, rate_limit=3, full_refresh=False):
        """
        Fetch and save chapters of novel in txt files.
        Only unsaved chapters will be fetched. Meaning a count of 5 will fetch and save the next 5 chapters after the latest chapter saved (if any exist).
        count: How many chapters to save [The variable itself represents the index upto which to save, default is -1 meaning the last element]
        rate_limit: The number of chapters to fetch before waiting 1 second. Default is 1 second for every 3 chapters.
        full_refresh: Ignore the chapters already downloaded and fetch all according to count. Default is False.
        """
        directory = self._create_folders()

        if not self.chapters:
            print('')
            self._get_chapters()

        start = 0
        if not full_refresh:
            start = self._get_latest_chapter(directory) + 1

        rate_limit_counter = 0
        for (chapter, link) in self.chapters[start:start+count]:
            url = self.base_url + link
            page = requests.get(url, headers=headers)
            chapter_page = BeautifulSoup(page.content, 'html.parser')
            save(chapter, chapter_page, directory)
            rate_limit_counter += 1
            if rate_limit_counter == rate_limit:
                rate_limit_counter = 0
                time.sleep(2)


# n = Novel(URL)
# print(n.link, n.title)
# n.save_chapters(count=2)
# n.get_chapters()
# print(n.chapters[:5])

