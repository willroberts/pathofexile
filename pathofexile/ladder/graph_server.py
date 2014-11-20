import flask
import analytics
from pathofexile.ladder import retrieve


app = flask.Flask(__name__)

@app.route('/api/<league_id>/<report_name>')
def get_report(league_id, report_name):
    report_functions = {
        'challenge_breakdown' : analytics.challenge_breakdown,
        'are_dead' : analytics.are_dead,
        'are_online' : analytics.are_online,
        'characters_per_account_breakdown' : analytics.characters_per_account_breakdown,
        'class_breakdown' : analytics.class_breakdown,
        'have_twitch_accounts' : analytics.have_twitch_accounts,
        'level_breakdown' : lambda x : analytics.level_breakdown(x, 1),
        'distinct_accounts' : analytics.distinct_accounts
    }
    ladder = retrieve(league_id)
    report = report_functions[report_name](ladder)

    #if the report is an int, it can't be jsonified
    if type(report) is int:
        report = { 'ladder_size': len(ladder), report_name: report,
                   'accounts' : analytics.distinct_accounts(ladder)}

    return flask.jsonify(report)

@app.route('/demo/<league_id>')
def demo_graphs(league_id):
    return flask.render_template("demo.html", league_id=league_id)

if __name__ == '__main__':
    app.run()