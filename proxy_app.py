import os
import flask


app = flask.Flask(__name__)


@app.route( '/hello', methods=['GET'] )
def hi():
    return flask.jsonify( {'hello': 'world'} )


@app.route( '/search_new_request', methods=['GET'] )
def search():



if __name__ == '__main__':
    if os.getenv('DEVBOX') == 'true':
        app.run( host='0.0.0.0', debug=True )
    else:
        app.run()
