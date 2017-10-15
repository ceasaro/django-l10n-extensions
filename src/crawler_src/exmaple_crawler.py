
class Crawler(object):
    def __init__(self, cache=None, depth=2):
        """
        depth: how many time it will bounce from page one (optional)
        cache: a basic cache controller (optional)
        """
        self.depth = depth
        self.content = {}
        self.cache = cache

    def crawl(self, url, no_cache=None):
        """
        url: where we start crawling, should be a complete URL like
        'http://www.intel.com/news/'
        no_cache: function returning True if the url should be refreshed
        """
        # u_parse = urlparse(url)
        self.domain = u_parse.netloc
        self.content[self.domain] = {}
        self.scheme = u_parse.scheme
        self.no_cache = no_cache
        self._crawl([u_parse.path], self.depth)

    def set(self, url, html):
        self.content[self.domain][url] = html
        if self.is_cacheable(url):
            self.cache.set(self.domain, url, html)

    def get(self, url):
        page = None
        if self.is_cacheable(url):
            page = self.cache.get(self.domain, url)
        if page is None:
            page = self.curl(url)
        else:
            print "cached url... [%s] %s" % (self.domain, url)
        return page

    def is_cacheable(self, url):
        return self.cache and self.no_cache \
               and not self.no_cache(url)

    def _crawl(self, urls, max_depth):
        n_urls = set()
        if max_depth:
            for url in urls:
                # do not crawl twice the same page
                if url not in self.content:
                    html = self.get(url)
                    self.set(url, html)
                    n_urls = n_urls.union(get_local_links(html, self.domain))
            self._crawl(n_urls, max_depth - 1)

    def curl(self, url):
        """
        return content at url.
        return empty string if response raise an HTTPError (not found, 500...)
        """
        try:
            print "retrieving url... [%s] %s" % (self.domain, url)
            req = urllib2.Request('%s://%s%s' % (self.scheme, self.domain, url))
            response = urllib2.urlopen(req)
            return response.read().decode('ascii', 'ignore')
        except urllib2.HTTPError, e:
            print "error [%s] %s: %s" % (self.domain, url, e)
            return ''
