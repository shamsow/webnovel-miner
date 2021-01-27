# Webnovel Miner

Uses `beautifulsoup4` to scrape a webnovel site and save the chapters as text files.

The motivation behing this project was to experiment with writing modules in Python and structure everything out into functions and objects.

This code is not intended to enable piracy. I did not use it to obtain any copyright material and neither should anyone else, which is why I did not include the site this code scrapes.

Since I avoided hardcoding any urls in this code, a `config.ini` file needs to placed in the `miner` module for this package to work.
```ini
miner/config.ini

[Website]
base_url: https://yourwebsite.com
choices: codes-for-novel
novel-code: novel-url

[System]
data_dir: name-of-folder-to-put-chapters

[Text]
exclude: comma-separated-strings-which-should-be-ignored-in-the-chapter-text

[Titles]
novel-code: novel-title
```

##### **** Still Under Construction ****