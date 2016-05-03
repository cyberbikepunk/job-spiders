""" Utility functions and classes for the test suite. """


from codecs import open
from requests import get
from scrapy import Request
from scrapy.http import HtmlResponse
from importlib import import_module
from slugify import slugify
from os.path import join, exists
from joby.settings import TEST_ASSETS_DIR


class WebpageCachingError(Exception):
    pass


# noinspection PyUnusedLocal
def make_offline_parser(spider, module_name, base_class_name, url, *loaders):
    module = import_module('joby.spiders.' + module_name)
    base_class = getattr(module, base_class_name)

    # noinspection PyShadowingNames
    class OfflineParser(base_class):
        def __init__(self, url, *loaders):
            self.filepath = join(TEST_ASSETS_DIR, slugify(url) + '.html')
            self.base_class = base_class
            self.url = url
            self.html = self._load_from_cache()
            self.request = Request(url=self.url)
            self.response = HtmlResponse(self.url, body=self.html, request=self.request)
            self.loaders = self._assign_loaders(loaders)

            super(OfflineParser, self).__init__(spider, self.response, **self.loaders)

        def _assign_loaders(self, loader_info):
            loaders = {}
            for item_name, item_class, loader_class in loader_info:
                loader = loader_class(item=item_class(), response=self.response)
                loaders.update({item_name: loader})
                return loaders

        def _load_from_cache(self):
            if not exists(self.filepath):
                self._save_to_cache()
            with open(self.filepath) as cache:
                return cache.read()

        def _save_to_cache(self):
            response = get(self.url)
            if response.status_code != 200:
                raise WebpageCachingError('Cannot download %s (%s)' % (self.url, response.status_code))
            else:
                with open(self.filepath, 'w+', response.encoding) as cache:
                    cache.write('<!-- ' + response.url + ' -->' + '\n')
                    cache.write(response.text)

        def __repr__(self):
            return '<Offline %s (%s)>' % (base_class_name, self.url)

    return OfflineParser(url, *loaders)
