# -*- coding: utf-8 -*-

import datetime, json, os
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


## experimentation ##


@app.route( '/hello1', methods=['GET'] )
def hi_a():
    """ Tests simple json response return. """
    return flask.jsonify( {'hello': 'world'} )


@app.route( '/hello2', methods=['GET'] )
def hi_b():
    """ Tests logging. """
    log.info( u'hi there' )
    return flask.jsonify( {'hello': 'world2'} )


@app.route( '/basic_auth', methods=['GET'] )
@basic_auth.required
def try_basic_auth():
    """ Tests basic-auth. """
    log.info( u'in proxy_app.try_basic_auth()' )
    return flask.jsonify( {'got': 'through'} )


@app.route( '/forbidden', methods=['GET'] )
def try_forbidden():
    """ Tests forbidden response. """
    log.debug( u'in proxy_app.try_forbidden()' )
    return flask.abort( 403 )


## real work ##


@app.route( u'/my_ip', methods=['GET'] )
def show_ip():
    """ Returns ip.
        Note: this was a test, but could be useful for debugging. """
    ip = flask.request.remote_addr
    log.debug( u'in proxy_app.show_ip(); remote_addr, `%s`' % ip )
    return flask.jsonify( {u'client_ip': ip} )


@app.route( u'/search_new_request', methods=['GET'] )
@basic_auth.required
def search():
    """ Searches for new requests. """
    log.debug( u'- in proxy_app; starting search()' )
    client_ip = flask.request.remote_addr
    log.debug( u'- in proxy_app.search(); client_ip, `%s`' % client_ip )
    if not client_ip in settings.LEGIT_IPS.keys():
        log.debug( u'- in proxy_app.search(); returning forbidden' )
        return flask.abort( 403 )
    log.debug( u'- in proxy_app; search(); ip legit' )
    db = db_handler.DB_Handler( log )
    result_dict = db.search_new_request()
    return_dict = {
        u'request_type': u'search_new_request',
        u'datetime': unicode( datetime.datetime.now() ),
        u'result': result_dict
        }
    return flask.jsonify( return_dict )




if __name__ == '__main__':
    if os.getenv('DEVBOX') == 'true':
        app.run( host='0.0.0.0', debug=True )
    else:
        app.run()
