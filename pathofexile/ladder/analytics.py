import collections
import time

import pathofexile.ladder

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
    ''' Returns the count of players who have Twitch accounts in
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
    ''' Returns the count of players who are dead in the given
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
    ''' Returns the count of players who are online in the given
    ladder.

    :param ladder: dict object from Ladder API (json response)
    :return: tuple of count (int) and percentage (float)
    '''
    count = 0
    for entry in ladder:
        if entry.get('online') is True:
            count += 1
    return count


def level_breakdown(ladder, bin_size):
    ''' Returns a dictionary whose keys are level groupings which map to the
    number of players who are have reached those levels. bin_size specifies
    the number of levels per group and the key corresponds to the level group
    starting at key*bin_size.

    :param ladder: dict object from Ladder API (json response)
    :param bin_size: the number of levels per group
    :return: dictionary of 'level group': 'player count' mappings
    '''
    counter = collections.Counter()
    for entry in ladder:
        counter[entry.get('character').get('level') / bin_size] += 1
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


def characters_per_account(ladder):
    """ Returns a Counter whose keys are account names which map to the
    number of characters that account has on the ladder.

    :param ladder: dict object from Ladder API (json response)
    :return: Counter of 'account names': '# of characters on ladder' mappings
    """
    return collections.Counter(
        [entry.get('account').get('name') for entry in ladder]
    )


def characters_per_account_breakdown(ladder):
    """ Returns a Counter whose keys are the # of characters which map
    to the total # of accounts that have that many characters on ladder.

    :param ladder: dict object from Ladder API (json response)
    :return: Counter of '# of characters': 'total # of accounts' mappings
    """
    return collections.Counter(characters_per_account(ladder).values())


def report(league, level_bin_size=10):
    ''' Puts together the data from the functions in this file, and prints it
    out to the user with some formatting. Retrieves the ladder for the
    requested league before showing analytics.

    :param league: name of the league to show analytics for
    :return: None (just prints)
    '''
    # get the ladder
    ladder = pathofexile.ladder.retrieve(league)
    ladder_size = len(ladder)

    # print a header
    print
    print league
    print '*' * len(league)

    # number of players with twitch accounts
    n = have_twitch_accounts(ladder)
    print 'Have Twitch accounts: %d (%.2f%%)' % (
        n,
        percentage(n, ladder_size=ladder_size),
    )

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
        print 'Dead: %d (%.2f%%)' % (
            n,
            percentage(n, ladder_size=ladder_size),
        )

    # level breakdown
    print 'Level breakdown:'
    levels = level_breakdown(ladder, level_bin_size)
    for level_group in sorted(levels.keys()):
        minimum_level = level_group * level_bin_size
        max_level = minimum_level + level_bin_size - 1
        max_level = max_level if max_level <= 100 else 100
        n = levels[level_group]
        if max_level == minimum_level:
            print '    %d: %d (%.2f%%)' % (
                max_level,
                n,
                percentage(n, ladder_size=ladder_size),
            )
        else:
            print '    %d-%d: %d (%.2f%%)' % (
                minimum_level,
                max_level,
                n,
                percentage(n, ladder_size=ladder_size),
            )

    # class breakdown
    print 'Class breakdown:'
    classes = class_breakdown(ladder)
    for class_name in classes:
        n = classes[class_name]
        print '    %s: %d (%.2f%%)' % (
            class_name,
            n,
            percentage(n, ladder_size=ladder_size),
        )

    # challenge breakdown
    print 'Challenge completion breakdown:'
    challenges = challenge_breakdown(ladder)
    for completion_tier in challenges:
        n = challenges[completion_tier]
        print '    %d challenges completed: %d (%.2f%%)' % (
            completion_tier,
            n,
            percentage(n, ladder_size=ladder_size),
        )

    # characters per account breakdown
    print 'Characters per account breakdown:'
    cpa_breakdown = characters_per_account_breakdown(ladder)
    num_accounts = sum(cpa_breakdown.values())
    for (k, v) in reversed(cpa_breakdown.items()):
        text = 'account has' if v == 1 else 'accounts have'
        print("    {:d} {:s} {:d} ladder characters ({:.2f}%)".
              format(v, text, k, percentage(v, ladder_size=num_accounts))
        )

    # top accounts
    print 'Top 5 accounts with most ladder characters:'
    iterator = enumerate(characters_per_account(ladder).most_common(5), 1)
    for i, (account, num_char) in iterator:
        print("    {:d}). {:s} ({:d})".format(i, account, num_char))

