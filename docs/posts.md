posts
=====


Shop Thread Embeds
------------------

This part of the codebase allows you to isolate the first post of a shop thread
while retaining the CSS and Javascript responsible for style and functionality.

It was developed to allow iframe-style embeds on http://www.poearena.com.

The first part of this is the PostIsolator object, which scrapes the HTML of a
shop thread and parses it out:


    >>> import pathofexile.forum.posts
    >>> p = pathofexile.forum.posts.PostIsolator(516116)
    >>> p.html

        <complete html for the _first post only_ of shop thread 516116>

I've also included an application server which filters out posts when a request
is sent to `/shop/<thread_number>`, and returns the isolated HTML. It uses the
Flask application server and the gunicorn HTTP server.

To get started, you'll need to set up your virtualenv. Follow the instructions
in the README, and then start the server:

    $ bash post_server.sh

Once it's running, you can test it by hitting this url:

    http://<your server>:8080/shop/<thread_number>

You can then embed that URL as an iframe from another website, using HTML or
BBCode.
