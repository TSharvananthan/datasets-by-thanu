import scraping_tools
import utils
import threading

urls = scraping_tools._gen_urls()
url_chunks = utils.chunks(urls, 12)

threads = [
    threading.Thread(
        target=scraping_tools.scrape_pages,
        args=(chunk,)
    )

    for chunk in url_chunks
]

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()