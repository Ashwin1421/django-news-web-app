from django.conf import settings


def getShareBaseURL(request):
        return {
            'FACEBOOK_SHARE': settings.FACEBOOK_SHARE_BASE_URL,
            'TWITTER_SHARE': settings.TWITTER_SHARE_BASE_URL
        }

class Constants:
    def __init__(self):
        self.country = ""
        self.search_term = ""
        self.sources = ""
        #default language setting
        self.language = "en"
        #default sorting by relevancy
        self.sortBy = "relevancy"
        self.category = ""

    def setCountry(self, country):
        self.country = country
    
    def getCountry(self):
        return self.country

    def setLang(self, language):
        self.language = language

    def setSources(self, sources):
        self.sources = sources

    def setSorting(self, sortBy):
        self.sortBy = sortBy

    def setSearchTerm(self, search_term):
        self.search_term = search_term 
    
    def getSearchTerm(self):
        return self.search_term