import pathofexile.analytics
import pathofexile.utilities


def main():
    leagues = ['Standard', 'Hardcore', 'One Month Race', 'One Month Race HC']
    for league in leagues:
        pathofexile.analytics.report(league)

if __name__ == '__main__':
    main()
