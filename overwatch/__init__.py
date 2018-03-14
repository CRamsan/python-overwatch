import urllib

from requests_html import HTMLSession

from .constants import (platforms, modes)
from .errors import (InvalidBattletag, InvalidCombination, InvalidStat,
                    InvalidHero, NotFound, InvalidArgument, UnexpectedBehaviour)

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
        self._model = {}
        self._r = session.get(self.url + platform + '/' + self._battletag)
        self.parse_page()

    '''
    Public methods to get a players available stats
    '''

    def comparison(self, mode='quickplay', stat='Time Played'):
        '''
        Show the different statistics by comparing them across all characters
        '''
        self._mode = self.get_mode(mode)
        tag = self._comparisons[stat]
        time = self.getHtmlForMode().find(f'div[data-category-id="overwatch.guid.{tag}"]')
        if len(time) == 0:
            return []
        time = time[0]
        return time.text.split('\n')

    def get_stats(self, mode='quickplay', hero='all'):
        '''
        Retrieve the different statistics based on the requested hero and the specified stat.
        '''
        self._mode = self.get_mode(mode)
        self._hero = hero.lower()
        self.error_check()
        return self.generate_stats()

    def achiements(self, achivementType='General'):
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
    def parse_page(self):
        for mode in constants.modes:
            html_mode = self.get_mode(mode)
            comparisons = self.getDictFromDropdown('comparisons', html_mode)
            comparisons_stats = self.comparison()
            heroes = self.getDictFromDropdown('stats', html_mode)
            model[mode] = {'comparisons' : comparisons_stats}
        achievements = self.getDictFromDropdown('achievements')
        self._mode = self.get_mode(mode)

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

    def getDictFromDropdown(self, selectId, pageSection = None):
        if pageSection == None:
            dropdownList = self._r.html.find(f'select[data-group-id="{selectId}"]')
        else:
            dropdownList = pageSection.find(f'select[data-group-id="{selectId}"]')
        if len(dropdownList) != 1:
            raise UnexpectedBehaviour('Found multiple dropdowns found.')
        optionList = dropdown.find('option')
        for option in optionList:
            text = option.text
            value = option.attrs['value']
            self._comparisons[text] = value
        return self._comparisons

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
    def comparisons(self, mode):
        return self._comparisons

    @property
    def heroes(self):
        return self._heroes

    @property
    def achievementTypes(self):
        return self._achievementTypes
