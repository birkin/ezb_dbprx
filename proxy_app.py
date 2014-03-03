import json, os
import flask
from ezb_dbprx.utils import logger_setup, db_handler


app = flask.Flask(__name__)
log = logger_setup.setup_logger()


@app.route( '/hello1', methods=['GET'] )
def hi_a():
    return flask.jsonify( {'hello': 'world'} )


@app.route( '/hello2', methods=['GET'] )
def hi_b():
    log.info( u'hi there' )
    return flask.jsonify( {'hello': 'world2'} )


@app.route( '/search_new_request', methods=['GET'] )
def search():
    log.info( u'starting search' )
    db = db_handler.DB_Handler( log )
    dict_list = db.search_new_request()
    return flask.jsonify( {u'output': dict_list} )
    # return flask.jsonify( {'will': 'do'} )


if __name__ == '__main__':
    if os.getenv('DEVBOX') == 'true':
        app.run( host='0.0.0.0', debug=True )
    else:
        app.run()
