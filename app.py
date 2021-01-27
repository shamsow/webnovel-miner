from miner.fetcher import Novel
from miner.config import config_data
codenames = config_data.get("Website", "choices").split(',')
titles = [config_data.get("Titles", codename) for codename in codenames]
for (title, codename) in zip(titles, codenames):
    print(f"{title} [ID: {codename}]")
selection = input("Type the ID of the novel you want to mine: ")


novel = Novel(selection)
# novel.save_chapters(count=2)
# print(fetcher.BASE_URL)