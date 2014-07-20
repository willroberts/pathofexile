import pathofexile.analytics
import pathofexile.update


def main():
    leagues = ['Standard', 'Hardcore', 'One Month Race', 'One Month Race HC']
    for league in leagues:
        ladder = pathofexile.update.get_ladder(league)
        pathofexile.analytics.report(league, ladder)

if __name__ == '__main__':
    main()
