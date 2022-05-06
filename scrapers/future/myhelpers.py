import urllib.request
from bs4 import BeautifulSoup


def get_soup(url):
    req = urllib.request.Request(url)
    site = urllib.request.urlopen(req)
    return BeautifulSoup(site.read(), "html.parser", from_encoding="utf-8")


def format_string(input_string):
    return input_string.strip().replace("\r\n", "").replace(" ", "")
