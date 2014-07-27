import flask
import logging

import posts

app = flask.Flask(__name__)
logging.basicConfig(filename='embed_server.log', level=logging.DEBUG)


@app.route('/')
def usage():
    return 'Usage: Send an HTTP GET to /shop/<thread number>'


@app.route('/shop/<shop_thread_id>')
def isolate_first_post(shop_thread_id):
    try:
        return posts.PostIsolator(shop_thread_id).html
    except Exception as e:
        logging.exception(e.message)

if __name__ == '__main__':
    app.run()
