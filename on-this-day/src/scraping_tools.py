from calendar import monthrange
from time import sleep

from bs4 import BeautifulSoup
from requests import get

def _gen_urls():
    categories = ["birthdays", "deaths", "events", "weddings"]
    months = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]
    days = [monthrange(2020, m)[1] for m in range(1, 13)]

    urls = []

    for category in categories:
        for month, last_day in zip(months, days):
            for day in range(1, last_day+1):
                u = f"https://www.onthisday.com/{category}/{month}/{day}" + "?p={}"
                urls.append(u)

    return urls

def _scrape_page(url: str):
    ''' Scrapes a page from onthisday.com according to date and category
    
    Note that there are two types of ways people are shown
        1) A plain text
        2) A special section with an image

    Both types of visuals are scraped and returned as one list

    Returns
    --------
    final (list) - A raw list of people
    '''
    sleep(0.5)

    print(url)

    soup = BeautifulSoup(get(url).content, "html.parser")

    p1 = [_.text for _ in soup.find("article").find_all("li")]
    p2 =  [_.find("p").text for _ in soup.find_all("div", {"class": "section--highlight"})]

    final = p1 + p2

    return final

def scrape_pages(urls: str):
    for url in urls:
        i = 1
        page_data = []
        while True:
            result = _scrape_page(url.format(i))

            if result == []:
                break

            if len(page_data) > 0:
                if result[0] == page_data[0]:
                    break

            i += 1
            page_data.extend(result)

        output_file = url.replace('https://www.onthisday.com/', '').replace('?p={}', '').replace("/", "-")

        with open(f"raw/{output_file}.txt", "w") as fp:
            fp.write("\n".join(page_data))