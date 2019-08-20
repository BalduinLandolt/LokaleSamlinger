"""
By Balduin Landolt

See Github for more info.

Run with exactly one command line parameter, that refers to the
Entry on Digitale Samlinger, (e.g. `7465`).
"""

import sys
import time
from bs4 import BeautifulSoup
from requests import get


def get_image_urls_from_thumbnails(url):
    res = []

    response = get(url)
    bs = BeautifulSoup(response.text, 'lxml')
    table = bs.find('table', attrs={'class':'ImageTable'})
    imgs = table.find_all('img')
    srcs = []
    for img in imgs:
        srcs.append('http://digitalesamlinger.hum.ku.dk'+img['src'])
    return res


def get_image_urls(urls):
    res = []
    for url in urls:
        res.extend(get_image_urls_from_thumbnails(url))
        # TODO: remove
        if len(res)>2:
            return res
        time.sleep(2)
    return res


def save_image(id, url):
    pass


def run_harvester(entry_id):
    print("Looking for: {}".format(entry_id))
    base_url = "http://digitalesamlinger.hum.ku.dk/Home/Samlingerne/"+entry_id
    sub_urls = get_sub_URLs(base_url)
    print(sub_urls)
    time.sleep(2)
    image_urls = get_image_urls(sub_urls);
    for i, img in enumerate(image_urls):
        save_image(i, img)
    # TODO: Do stuff.


def get_sub_URLs(base):
    response = get(base)
    bs = BeautifulSoup(response.text, 'lxml')
    all_links = bs.select('a')
    links_with_href = []
    for link in all_links:
        if link.has_attr('href'):
            links_with_href.append(link)
    hrefs = []
    for link in links_with_href:
        if link['href'].startswith('/Home/Samlingerne/'):
            hrefs.append('http://digitalesamlinger.hum.ku.dk'+link['href'])
    # remove previous and next manuscript
    hrefs.pop(0);
    hrefs.pop(0);
    # put the last one in the beginning
    hrefs.insert(0, hrefs.pop(len(hrefs)-1))
    # TODO: not every manuscript has inverted order
    res = []
    for ref in hrefs:
        res.append(ref)
        res.append(ref+'/2')
        # TODO: not every manuscript has multiple pages with thumbnails
    return res


if __name__ == "__main__":
    print("Running...")
    print("Number of Arguments: {}".format(len(sys.argv)))
    print("Arguments: {}".format(sys.argv))
    if len(sys.argv) != 2:
        print("Unexpected number of arguments.\nAbort.")
        exit(-1)
    run_harvester(sys.argv[1])
    print("Done.")
