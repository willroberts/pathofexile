import requests

'''
Path of Exile API Client
- Minimal implementations of the Path of Exile Developer API

Note: Exceptions and error responses are not fully implemented yet
'''


class InvalidParameterError(Exception):
    pass


class InvalidLeagueTypeError(InvalidParameterError):
    pass


class InvalidLeagueIdError(InvalidParameterError):
    pass


class InvalidLadderInclusionError(InvalidParameterError):
    pass


class InvalidLadderLimitError(InvalidParameterError):
    pass


class InvalidLadderOffsetError(InvalidParameterError):
    pass


class InvalidLeagueRuleIdError(InvalidParameterError):
    pass


class InvalidLadderIdError(InvalidParameterError):
    pass


class RateLimitExceededError(Exception):
    pass


class Codes(object):
    returns = {
        '200': 'OK',
        '400': 'Bad Request',
        '404': 'Not Found',
        '429': 'Too Many Requests',
        '500': 'Internal Server Error',
    }

    errors = {
        '1': 'Resource Not Found',
        '2': 'Invalid Query',
        '3': 'Rate Limit Exceeded',
        '4': 'Internal Error',
        '5': 'Unexpected Content Type',
        '6': 'Forbidden',
    }


def list_leagues(league_type='all'):
    ''' Get a list of current leagues. Returns no more than 50 entries.

    :param league_type: Possible values, "all" to retrieve all leagues (the
        default), or "event" to retrieve event leagues.
    :return: A list of all league details
    '''
    if league_type not in ['all', 'event']:
        raise InvalidLeagueTypeError

    endpoint = 'http://api.pathofexile.com/leagues'
    params = {'type': league_type}

    r = requests.get(endpoint, params=params)
    return r.json()


def get_league(league_id, ladder=0, ladder_limit=20, ladder_offset=0):
    ''' Get a single league by id.

    :param league_id: The id (name) of the league
    :param ladder: Set to 1 to include the ladder in the response. The ladder
        will be in included in the "ladder" key. Defaults to 0, excluding the
        ladder. Please note that the ladder can be retrieved using the ladder
        resource, and that retrieving it using the league API is just an
        optimization that can be used if you are requesting the league anyway.
    :param ladder_limit: When including the ladder with ladder=1, specifies
        the number of ladder entries to include. Default: 20, Max: 200.
    :param ladder_offset: When including the ladder with ladder=1, this
        specifies the offset to the first ladder entry to include. Default: 0.
    :return: A dictionary of league details
    '''
    if not isinstance(league_id, basestring):
        raise InvalidLeagueIdError
    if ladder not in [0, 1]:
        raise InvalidLadderInclusionError
    if not ladder_limit > 0 or not ladder_limit <= 200:
        raise InvalidLadderLimitError
    if not ladder_offset >= 0 or not ladder_offset < 15000:
        raise InvalidLadderOffsetError

    endpoint = 'http://api.pathofexile.com/leagues/%s' % league_id
    params = {
        'id': league_id,
        'ladder': ladder,
        'ladderLimit': ladder_limit,
        'ladderOffset': ladder_offset,
    }

    r = requests.get(endpoint, params=params)
    return r.json()


def list_league_rules():
    ''' Get a list of all possible league rules.

    :return: A list of all league rules
    '''
    endpoint = 'http://api.pathofexile.com/league-rules'
    params = {}

    r = requests.get(endpoint, params=params)
    return r.json()


def get_league_rule(league_rule_id):
    ''' Get a single league rule by id.

    :param league_rule_id: the rule id
    :return: A dictionary of league rule details
    '''
    try:
        league_rule_id = int(league_rule_id)
    except:
        raise InvalidLeagueRuleIdError

    endpoint = 'http://api.pathofexile.com/league-rules/%d' % league_rule_id
    params = {}

    r = requests.get(endpoint, params=params)
    return r.json()


def get_ladder(ladder_id, ladder_limit=20, ladder_offset=0):
    ''' Get a ladder by league id. There is a restriction in place on the last
    ladder entry you are able to retrieve which is set to 15000.

    :param ladder_id: The id (name) of the league for the ladder you want
        to retrieve.
    :param ladder_limit: Specifies the number of ladder entries to include.
        Default: 20, Max: 200.
    :param ladder_offset: Specifies the offset to the first ladder entry to
        include. Default: 0.
    :return: A list of ladder players
    '''
    if not isinstance(ladder_id, basestring):
        raise InvalidLadderIdError
    if not ladder_limit > 0 or not ladder_limit <= 200:
        raise InvalidLadderLimitError
    if not ladder_offset >= 0 or not ladder_offset < 15000:
        raise InvalidLadderOffsetError

    endpoint = 'http://api.pathofexile.com/ladders'
    params = {'id': ladder_id, 'limit': ladder_limit, 'offset': ladder_offset}

    r = requests.get(endpoint, params=params)
    if r.status_code == '429':
        raise RateLimitExceededError
    else:
        return r.json()
