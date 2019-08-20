"""
By Balduin Landolt

See Github for more info.

Run with exactly two command line parameter, that refer to the
Entry on Digitale Samlinger, and give a name to the output (e.g. `7465 AM_634_4to`).
"""

import sys
import os
import time
from urllib import request
from urllib import parse

from bs4 import BeautifulSoup
from requests import get


def get_image_urls_from_thumbnails(url):
    print("Checking: {}".format(url))
    srcs = []

    response = get(url)
    if response.status_code != 200:
        return srcs
    bs = BeautifulSoup(response.text, 'lxml')
    table = bs.find('table', attrs={'class':'ImageTable'})
    imgs = table.find_all('img')
    for img in imgs:
        link = 'http://digitalesamlinger.hum.ku.dk'+parse.quote(img['src'])
        if not link in srcs:
            srcs.append(link)
    print("Found {} image links.".format(len(srcs)))
    return srcs


def remove_blanks(links):
    while "http://digitalesamlinger.hum.ku.dkdata%3Aimage/gif%3Bbase64%2CR0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7" in links:
        links.remove("http://digitalesamlinger.hum.ku.dkdata%3Aimage/gif%3Bbase64%2CR0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7")
    return links


def get_image_urls(urls):
    res = []
    for url in urls:
        res.extend(get_image_urls_from_thumbnails(url))
        # TODO: remove
        #if len(res)>2:
        #    return res
        time.sleep(.5)
    print("Overall Image URLs: {}".format(len(res)))
    res = remove_blanks(res)
    print("Removed blanks. {} left.".format(len(res)))
    return res


def save_image(id, url, name):
    path = 'out/'+name+'/'
    if not os.path.isdir(path):
        os.mkdir(path)
    file_name = "{}___{:04d}.jpg".format(name, id)
    print(url)
    response = request.urlopen(url)
    data = response.read()
    with open(path+file_name, 'wb') as file:
        file.write(data)


def run_harvester(entry_id, name):
    print("Looking for: {}".format(entry_id))
    base_url = "http://digitalesamlinger.hum.ku.dk/Home/Samlingerne/"+entry_id
    sub_urls = get_sub_URLs(base_url)
    print(sub_urls)
    time.sleep(.5)
    image_urls = get_image_urls(sub_urls);
    for i, img in enumerate(image_urls):
        save_image(i, img, name)
        time.sleep(.5)
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
    print("Got {} sub-links.".format(len(res)))
    return res


if __name__ == "__main__":
    print("Running...")
    i = 10
    print("Number of Arguments: {}".format(len(sys.argv)))
    print("Arguments: {}".format(sys.argv))
    if len(sys.argv) != 3:
        print("Unexpected number of arguments.\nAbort.")
        exit(-1)
    run_harvester(sys.argv[1], sys.argv[2])
    print("Done.")
