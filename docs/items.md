Items
=====

Relevant files:
* `pathofexile/forum/items.py`
* `pathofexile/forum/item_server.py`
* `pathofexile/forum/templates/items.html`
* `pathofexile/forum/assets/css/item_server.css`
* `item_server.sh`


Summary
-------

On the Path of Exile forums, shop threads include Javascript code which
contains a list of all items in the thread, as well as their metadata.

`items.py` is responsible for parsing the items from a shop thread, and it
returns them as a list of Item() objects. Item() is a custom class which
contains logic for parsing items, grouping sockets, resizing images, and more.

`item_server.py` is a small HTTP server which listens for requests to
`http://<server address>:8080/shop/<shop thread number>`, and then returns
rendered HTML content of the items in the requested thread. This HTML is
constructed and styled by `items.html` and `item_server.css`. To start the
server in the background, run `item_server.sh` when the virtualenv is active.


The Item() Class
----------------

    >>> 
