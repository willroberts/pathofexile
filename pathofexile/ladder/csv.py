import csv
import os
import requests


def download_ladder_csv(league):
    ''' Downloads the entire ladder for a league in CSV format. Takes around 6
    seconds on average, which is faster than pulling the ladder from the API
    sequentially (75 seconds) or concurrently (20 seconds). The downside is
    that CSV ladder data does not include Twitch information or challenge
    completion information.

    CSV format:

        LoginStatus,Rank,Account,Character,Class,Level,Experience,Dead

    :param league: League for which to retrieve the ladder CSV
    :return: None (writes to file)
    '''
    base_url = 'http://www.pathofexile.com/ladder/export-csv/league/%s/index/1'
    url = base_url % league
    cache_dir = '.ladder_cache'
    csv_file = '%s/%s.csv' % (cache_dir, league.replace(' ', ''))
    r = requests.get(url)
    if not os.path.exists(cache_dir):
        os.mkdir(cache_dir)
    with open(csv_file, 'w') as f:
        f.write(r.content)
