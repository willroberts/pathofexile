pathofexile
===========

A Python framework for building tools related to Path of Exile.

Includes a complete implementation of the Path of Exile Developer API, tools
for analytics, and tools for forum scraping.

Pull requests are highly encouraged! If you see room for improvement, fork the
code, commit your patch, and then send a pull request so I can merge it in.


Features <a name='features'></a>
--------
* Full implementation of the Path of Exile API
* Forum parsing code for shop threads
* Utilities to make pulling useful data faster and easier
* Pickle-based caching to avoid repeat lookups
* Analytics utilities for printing ladder statistics


Documentation
-------------

1. <a href='docs/api.md'>Core API</a>


Installing Dependencies
-----------------------

Install virtualenv

    sudo pip install virtualenv

Create a virtualenv

    virtualenv env

Activate it

    source env/bin/activate

Install the Python library dependencies:

    pip install -r requirements.txt


To Do
-----

Documentation:

* Add general documentation for the included tools and their usage
* Add/expand in-code documentation (docstrings)

Core API:

* Use the documented return codes and error codes in the core API
  * Use the Codes.returns[429] error message when the rate limit is exceeded

Analytics:

* Add analytics for the number of ladder characters per account
  * 1 account has 5 ladder characters, 10 accounts have 4, etc.
* Write graph generation code for analytics
  * See http://i.imgur.com/lp0ZPCH.jpg

Forum Parsing:

* Continue to improve HTML/CSS/JS assets to improve visual style
  * See http://i.imgur.com/fOX0MFR.png

PVP:

* Write code to generate and manage tournament brackets
