import collections
import time

'''
Path of Exile API Client
- Analytics
'''


def percentage(player_count, ladder_size=15000):
    ''' Returns the percentage of players given a player count and a ladder
    size. Converts both to floats before division to retain precision.

    :param player_count: int number of players
    :param ladder_size: int number of players in the relevant ladder
    :return: float percentage of players
    '''
    return float(player_count) / float(ladder_size) * 100.0


def have_twitch_accounts(ladder):
    ''' Returns the count and percentage of players who have Twitch accounts in
    the given ladder.

    :param ladder: dict object from Ladder API (json response)
    :return: tuple of count (int) and percentage (float)
    '''
    count = 0
    for entry in ladder:
        if 'twitch' in entry.get('account'):
            count += 1
    return count


def are_dead(ladder):
    ''' Returns the count and percentage of players who are dead in the given
    ladder. Will always return 0 for non-hardcore leagues.

    :param ladder: dict object from Ladder API (json response)
    :return: tuple of count (int) and percentage (float)
    '''
    count = 0
    for entry in ladder:
        if entry.get('dead') is True:
            count += 1
    return count


def are_online(ladder):
    ''' Returns the count and percentage of players who are online in the given
    ladder.

    :param ladder: dict object from Ladder API (json response)
    :return: tuple of count (int) and percentage (float)
    '''
    count = 0
    for entry in ladder:
        if entry.get('online') is True:
            count += 1
    return count


def level_breakdown(ladder):
    ''' Returns a dictionary whose keys are level groupings which map to the
    number of players who are have reached those levels. The keys range from 0
    to 10, and they represent the following level groups:

        0:  0 through  9        6: 60 through 69
        1: 10 through 19        7: 70 through 79
        2: 20 through 29        8: 80 through 89
        3: 30 through 39        9: 90 through 99
        4: 40 through 49       10: 100
        5: 50 through 59

    :param ladder: dict object from Ladder API (json response)
    :return: dictionary of 'level group': 'player count' mappings
    '''
    counter = collections.Counter()
    for entry in ladder:
        counter[entry.get('character').get('level') / 10] += 1
    return counter


def class_breakdown(ladder):
    ''' Returns a dictionary whose keys are class names which map to the
    number of players who are playing those classes.

    :param ladder: dict object from Ladder API (json response)
    :return: dictionary of 'class': 'player count' mappings
    '''
    counter = collections.Counter()
    for entry in ladder:
        counter[entry.get('character').get('class')] += 1
    return counter


def challenge_breakdown(ladder):
    ''' Returns a dictionary whose keys are numbers of challenges completed
    (0 through 8) which map to the number of players who have completed that
    number of challenges.

    :param ladder: dict object from Ladder API (json response)
    :return: dictionary of 'challenges completed': 'player count' mappings
    '''
    counter = collections.Counter()
    for entry in ladder:
        counter[entry.get('account').get('challenges').get('total')] += 1
    return counter


def report(league, ladder):
    ''' Puts together the data from the functions in this file, and prints it
    out to the user with some formatting.

    :param ladder: dict object from Ladder API (json response)
    :return: None (just prints)
    '''
    # print a header
    print
    print league
    print '*' * len(league)

    # number of players with twitch accounts
    n = have_twitch_accounts(ladder)
    print 'Have Twitch accounts: %d (%.2f%%)' % (n, percentage(n))

    # number of players online
    n = are_online(ladder)
    print 'Online (%s UTC): %d (%.2f%%)' % (
        time.strftime('%H:%M', time.gmtime()),
        n,
        percentage(n),
    )

    # number of dead players
    n = are_dead(ladder)
    if 'HC' in league or 'Hardcore' in league:
        print 'Dead: %d (%.2f%%)' % (n, percentage(n))

    # level breakdown
    print 'Level breakdown:'
    levels = level_breakdown(ladder)
    for level_group in levels:
        minimum_level = level_group * 10
        n = levels[level_group]
        print '    %d+: %d (%.2f%%)' % (minimum_level, n, percentage(n))

    # class breakdown
    print 'Class breakdown:'
    classes = class_breakdown(ladder)
    for class_name in classes:
        n = classes[class_name]
        print '    %s: %d (%.2f%%)' % (class_name, n, percentage(n))

    # challenge breakdown
    print 'Challenge completion breakdown:'
    challenges = challenge_breakdown(ladder)
    for completion_tier in challenges:
        n = challenges[completion_tier]
        print '    %d challenges completed: %d (%.2f%%)' % (
            completion_tier,
            n,
            percentage(n),
        )
