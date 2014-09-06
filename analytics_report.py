import pathofexile.api
import pathofexile.ladder.analytics


def main():
    # set default leagues
    leagues = ['Standard', 'Hardcore']
    # try to get a list of updated leagues from the API
    try:
        leagues = [league.get('id') for league in pathofexile.api.get_leagues()]
    except:
        pass
    for league in leagues:
        pathofexile.ladder.analytics.report(league)

if __name__ == '__main__':
    main()
