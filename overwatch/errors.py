class InvalidStat(Exception):
    """
    Raise when 'stat' key word argument is not recognized
    """
    pass


class InvalidHero(Exception):
    """
    Raise when 'hero' key word argument is not recognized
    """
    pass


class InvalidCombination(Exception):
    """
    Raise when 'filter' and 'hero' key word arguments
    are an invalid combination.
    """
    pass


class InvalidBattletag(Exception):
    """
    Raise when 'battletag' key word argument is none 
    """
    pass

class InvalidArgument(Exception):
    """
    Raise when a provider argument does not belong the list of expected values 
    """
    pass


class NotFound(Exception):
    """
    Raise when stats could not be found
    """
    pass

class UnexpectedBehaviour(Exception):
    """
    Raise when we identify unexpected behaviour is found. This usually signals a bug.
    """
    pass
