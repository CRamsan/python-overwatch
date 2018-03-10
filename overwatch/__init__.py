import urllib

from requests_html import HTMLSession

from .constants import (platforms, heroes, modes, comparisons, achievementTypes)
from .errors import (InvalidBattletag, InvalidCombination, InvalidStat,
                    InvalidHero, NotFound, InvalidArgument)

session = HTMLSession()

class Overwatch:

    '''
    Constructor
    '''
    def __init__(self, battletag=None, platform='pc'):
        self.url = 'https://playoverwatch.com/en-us/career/'
        if platform == 'pc':
            try:
                self._battletag = urllib.parse.quote(battletag.replace('#', '-'))
            except AttributeError:
                raise InvalidBattletag(f'battletag="{battletag}" is invalid')
        elif platform not in constants.platforms:
                raise InvalidArgument(f'platform="{platform}" is invalid')
        else:
            self._battletag = urllib.parse.quote(battletag)
        self._platform = platform
        self._comparisons = []
        self._stats = []
        furl = self.url + platform + '/' + self._battletag
        print (furl)
        self._r = session.get(furl)

    '''
    Public methods to get a players available stats
    '''

    def comparison(self, mode='quickplay', stat='Time Played'):
        '''
        Show the different statistics by comparing them across all characters
        '''
        self._mode = self.get_mode(mode)
        tag = constants.comparisons[stat]
        time = self.getHtmlForMode().find(f'div[data-category-id="overwatch.guid.{tag}"]')
        if len(time) == 0:
            return []
        time = time[0]
        return time.text.split('\n')

    def get_stats(self, mode='quickplay', hero='all', stat='best'):
        '''
        Retrieve the different statistics based on the requested hero and the specified stat.
        '''
        self._mode = self.get_mode(mode)
        self._hero = hero.lower()
        self._stat = stat.title()
        self.error_check()
        return self.generate_stats()

    def achiements(self, mode='quickplay', achivementType='General'):
        '''
        Retrieve a list of available and acquired achivements.
        Currently this function is not implemented.
        '''
        
        '''
        self._mode = self.get_mode(mode)
        tag = constants.achievementTypes[achivementType]
        time = self.getHtmlForMode().find(f'div[data-category-id="overwatch.achievementCategory.{tag}"]')
        if len(time) == 0:
            return []
        time = time[0]
        return time.text.split('\n')
        '''
        return []

    '''
    Internal methods
    '''
    def generate_stats(self):
        html = self.getHtmlForMode().find(f'div[data-category-id="{heroes[self._hero]}"]')
        if len(html) == 0:
            return []
        hero = html[0]
        cards = hero.find('.card-stat-block')
        for card in cards:
            if card.text.startswith(self._stat):
                return card.text.split("\n")[1:]

    def get_mode(self, mode):
        if mode not in constants.modes:
            raise InvalidArgument(f'mode="{mode}" is invalid')
        return (mode)

    def error_check(self):
        if self._stat == "Hero Specific" and self._hero == 'all':
            raise InvalidCombination(f"'{self._stat}' and '{self._hero}'"
                                     " are not valid stat combinations")
        if self._stat == "Miscellaneous" and self._hero != 'all':
            raise InvalidCombination(f"'{self._stat}' and '{self._hero}'"
                                     " are not valid stat combinations")
        if self._hero not in constants.heroes.keys():
            raise InvalidArgument(f'hero="{hero}" is invalid')
        if self._stat not in self.stats:
            raise InvalidStat(f'stat="{self._stat}" is invalid.')

    def error_handler(func):
        def decorator(self, *args):
            try:
                results = func(self, *args)
                return results
            except KeyError:
                raise InvalidHero(f'hero="{self._hero}" is invalid.')
        return decorator

    def getHtmlForMode(self):
        html = self._r.html.find(f'div[id="{self._mode}"]')
        if len(html) != 1:
            raise UnexpectedBehaviour('Finding the element for this game mode returned more than 1 element')
        return html[0]

    '''
    Properties to know supported parameters.

    This functions will need to parse the source html and therefore it will require to make a network call.

    '''

    @property
    def platforms(self):
        return list(constants.platforms)

    @property
    def modes(self):
        return list(constants.modes)

    @property
    def heroes(self):
        return list(constants.heroes.keys())

    @property
    def stats(self):
        if len(self._stats) == 0:
            stats = self._r.html.find(".stat-title")
            self._stats = list(set((stat.text for stat in stats)))
        return self._stats

    @property
    def comparisons(self):
        return list(constants.comparisons.keys())

    @property
    def achievementTypes(self):
        return list(constants.achievementTypes.keys())
