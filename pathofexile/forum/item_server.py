import flask
import os
import items

app = flask.Flask(__name__)


@app.route('/')
def usage():
    return 'Usage: Send an HTTP GET to /shop/your_thread_number'


@app.route('/style.css')
def style():
    ''' To do: use something more suitable for static content to serve this
    '''
    with open('pathofexile/forum/assets/css/item_server.css', 'r') as f:
        return f.read()


@app.route('/shop/<shop_thread_id>')
def find_items(shop_thread_id):
    return items.show_items(shop_thread_id)

if __name__ == '__main__':
    app.run()
