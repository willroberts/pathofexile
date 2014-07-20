pathofexile
===========

API Client for the Path of Exile Developer API

Includes some analytics tools and pickle-based caching.


Features
--------
* Full implementation of the [Path of Exile Developer API](http://www.pathofexile.com/developer/docs/api)
* Utilities to make pulling useful data easier
* Concurrent request mapping to speed up retrieval
* Pickle-based caching to avoid repeat lookups
* Analytics utilities for printing ladder statistics


Coming Soon
-----------
* RRD graphs for online player counts


Installing Dependencies
-----------------------

If you're on Ubuntu Linux, install the dependency packages:

    sudo apt-get install libxml2-dev libcairo2-dev python-cairo-dev libpango1.0-dev librrd-dev

Install virtualenv

    sudo pip install virtualenv

Create a virtualenv

    virtualenv env

Activate it

    source env/bin/activate

Install the Python library dependencies:

    pip install -r requirements.txt


Getting Started
---------------

    $ python

    >>> import pathofexile.api
    >>> pathofexile.api.list_leagues()
    <list of leagues and metadata>

    >>> import pathofexile.update
    >>> import pathofexile.analytics
    >>> ladder = pathofexile.update.get_ladder('Standard')
    >>> pathofexile.analytics.show_report('Standard', ladder)
    <big analytics report for requested league>
