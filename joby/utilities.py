""" Utility classes and functions. """


from bs4 import BeautifulSoup


class Parser(object):
    parser_engine = 'lxml'
    encoding = 'utf-8'

    def __init__(self, spider, response, **loaders):
        self.spider = spider
        self.response = response
        self.soup = BeautifulSoup(response.body, self.parser_engine)

        for name, loader in loaders.items():
            setattr(self, name, loader)
