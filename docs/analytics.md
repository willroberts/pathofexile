Analytics
=========

Relevant files:

* `pathofexile/ladder/analytics.py`


Summary
-------

Leverages the code from the <a href="ladders.md">Ladders</a> section to
generate statistics about the players in the given league.


Printing League Statistics
--------------------------

    >>> import pathofexile.analytics
    >>> pathofexile.analytics.report('Standard')

    Standard
    ********
    Have Twitch accounts: 2744 (18.29%)
    Online (21:01 UTC): 558 (3.72%)
    Level breakdown:
        80-89: 5280 (35.20%)
        90-99: 9638 (64.25%)
        100: 82 (0.55%)
    Class breakdown:
        Scion: 2702 (18.01%)
        Templar: 1012 (6.75%)
        Ranger: 1985 (13.23%)
        Witch: 3108 (20.72%)
        Duelist: 1646 (10.97%)
        Shadow: 1559 (10.39%)
        Marauder: 2988 (19.92%)
    Challenge completion breakdown:
        0 challenges completed: 13439 (89.59%)
        1 challenges completed: 1158 (7.72%)
        2 challenges completed: 278 (1.85%)
        3 challenges completed: 95 (0.63%)
        4 challenges completed: 26 (0.17%)
        5 challenges completed: 4 (0.03%)
    Characters per account breakdown:
        1 account has 12 ladder characters (0.01%)
        1 account has 11 ladder characters (0.01%)
        2 accounts have 9 ladder characters (0.02%)
        7 accounts have 8 ladder characters (0.06%)
        8 accounts have 7 ladder characters (0.07%)
        19 accounts have 6 ladder characters (0.17%)
        48 accounts have 5 ladder characters (0.43%)
        175 accounts have 4 ladder characters (1.57%)
        557 accounts have 3 ladder characters (4.99%)
        1780 accounts have 2 ladder characters (15.95%)
        8562 accounts have 1 ladder characters (76.72%)
    Top 5 accounts with most ladder characters:
        1). Sauron_is_Coming (12)
        2). HegemonyTV (11)
        3). moostrenko (9)
        4). AkamuCZ (9)
        5). nLLss (8)
