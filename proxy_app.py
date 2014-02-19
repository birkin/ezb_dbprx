import os
import flask
from ezb_dbprx.utils import logger


app = flask.Flask(__name__)
log = logger.setup_logger()


@app.route( '/hello', methods=['GET'] )
def hi():
    return flask.jsonify( {'hello': 'world'} )


@app.route( '/hello2', methods=['GET'] )
def hi():
    log.info( u'hi there' )
    return flask.jsonify( {'hello': 'world2'} )





@app.route( '/search_new_request', methods=['GET'] )
def search():
    return flask.jsonify( {'hello': 'there'} )


if __name__ == '__main__':
    if os.getenv('DEVBOX') == 'true':
        app.run( host='0.0.0.0', debug=True )
    else:
        app.run()
