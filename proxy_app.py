# -*- coding: utf-8 -*-

import json, os
import flask
from ezb_dbprx.config import settings
from ezb_dbprx.utils import logger_setup, db_handler
from flask.ext.basicauth import BasicAuth  # http://flask-basicauth.readthedocs.org/en/latest/


## setup
app = flask.Flask(__name__)
log = logger_setup.setup_logger()
#
app.config['BASIC_AUTH_USERNAME'] = settings.BASIC_AUTH_USERNAME
app.config['BASIC_AUTH_PASSWORD'] = settings.BASIC_AUTH_PASSWORD
basic_auth = BasicAuth(app)


@app.route( '/hello1', methods=['GET'] )
def hi_a():
    return flask.jsonify( {'hello': 'world'} )


@app.route( '/hello2', methods=['GET'] )
def hi_b():
    log.info( u'hi there' )
    return flask.jsonify( {'hello': 'world2'} )


@app.route( '/basic_auth', methods=['GET'] )
@basic_auth.required
def try_basic_auth():
    """ basic-auth test """
    log.info( u'in proxy_app.try_basic_auth()' )
    return flask.jsonify( {'got': 'through'} )




@app.route( '/search_new_request', methods=['GET'] )
@basic_auth.required
def search():
    log.info( u'- in proxy_app; starting search()' )
    db = db_handler.DB_Handler( log )
    dict_list = db.search_new_request()
    return flask.jsonify( {u'output': dict_list} )




if __name__ == '__main__':
    if os.getenv('DEVBOX') == 'true':
        app.run( host='0.0.0.0', debug=True )
    else:
        app.run()
