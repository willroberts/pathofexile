import pathofexile.ladder.analytics


def main():
    leagues = ['Standard', 'Hardcore', 'One Month Race', 'One Month Race HC']
    for league in leagues:
        pathofexile.ladder.analytics.report(league)

if __name__ == '__main__':
    main()
