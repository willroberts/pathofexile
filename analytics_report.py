import pathofexile.api
import pathofexile.ladder.analytics


def main():
    leagues = [league.get('id') for league in pathofexile.api.get_leagues()] or\
              ['Standard', 'Hardcore']
    for league in leagues:
        pathofexile.ladder.analytics.report(league)

if __name__ == '__main__':
    main()
