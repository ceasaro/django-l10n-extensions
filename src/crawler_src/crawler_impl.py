# -*- coding: utf-8 -*-
# filename: crawler.py

import urllib2

from bs4 import BeautifulSoup
from urlparse import urlparse


class Crawler(object):
    def __init__(self, depth=2):
        """
        depth: how many time it will bounce from page one (optional)
        """
        self.depth = depth
        self.domain = ''
        self.msg_ids = {}
        self.visited = []

    def crawl(self, url):
        """
        url: where we start crawling, should be a complete URL like
        'http://www.intel.com/news/'
        """
        parse_result = urlparse(url)
        self.domain = parse_result.netloc
        self.scheme = parse_result.scheme
        self._crawl([url], self.depth)

    def _crawl(self, urls, max_depth):
        n_urls = set()
        if max_depth:
            for url in urls:
                # do not crawl twice the same page
                if url not in self.visited:
                    n_urls = n_urls.union(self.get_links(url))
            self._crawl(n_urls, max_depth-1)

    def get_page(self, url):
        """
        return content at url.
        return empty string if response raise an HTTPError (not found, 500...)
        """
        try:
            print ("retrieving url... {}".format(url))
            data = urllib2.urlopen(url)
            return BeautifulSoup(data.read(), "html.parser")
        except Exception as e:
            print ("error {}: {}".format(url, e))
            return None

    def get_links(self, url):
        """
        Read through HTML content and returns a tuple of links
        internal to the given domain
        """
        page = self.get_page(url)
        a_tags = page.find_all('a')
        urls = set()
        for a_tag in a_tags:
            try:
                href = a_tag['href']
                if href.startswith('/'):
                    url = "{}://{}{}".format(self.scheme, self.domain, href)
                elif href.startswith(self.domain):
                    url = href
                if url not in self.visited:
                    urls.add(url)
            except KeyError:
                pass  # no href found on a-tag

        return urls


