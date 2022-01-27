
class DLsiteCompanyCrawler:

    def __init__(self, code='', title=''):
        self.code = code
        self.title = title

        self.html = None
        self.bs4 = None