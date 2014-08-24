import pathofexile.api


def get_leagues(race_leagues_only=False):
    league_type = 'event' if race_leagues_only else 'all'
    leagues = pathofexile.api.get_leagues(league_type=league_type)
    for league in [l.get('id') for l in leagues]:
        print league
    
if __name__ == '__main__':
    get_leagues()
