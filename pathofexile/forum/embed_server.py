import flask
import posts

app = flask.Flask(__name__)


@app.route('/shop/<shop_thread_id>')
def isolate_first_post(shop_thread_id):
    return posts.PostIsolator(shop_thread_id).html

if __name__ == '__main__':
    app.run()
