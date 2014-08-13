Items
=====

Retrieving items from shop threads:


    >>> import pathofexile.forum
    >>> import pprint
    >>> items = pathofexile.forum.find_items(923014)
    >>> pprint.pprint(items)
    
    [
        {
            u'corrupted': False,
            u'explicitMods': [
                u'10% increased Attack Speed',
                u'+20 to Evasion Rating',
                u'+23 to maximum Mana',
                u'42% of Physical Damage Converted to Fire Damage'
            ],
            u'flavourText': [
                u'Molten feathers, veiled spark,\r',
                u'Hissing arrows from the dark.'
            ],
            u'frameType': 3,
            u'h': 3,
            u'icon': u'http://webcdn.pathofexile.com/image/Art/2DItems/Quivers/BlackgleamAlt.png',
            u'identified': True,
            u'implicitMods': [
                u'Adds 4-8 Fire Damage to attacks with Bows'
            ],
            u'league': u'Unknown',
            u'name': u'Blackgleam',
            u'requirements': [
                {
                    u'displayMode': 0,
                    u'name': u'Level',
                    u'values': [
                        [
                            u'22',
                            0
                        ]
                    ]
                }
            ],
            u'socketedItems': [],
            u'sockets': [],
            u'support': True,
            u'typeLine': u'Fire Arrow Quiver',
            u'verified': True,
            u'w': 2
        },
        ...
    ]
