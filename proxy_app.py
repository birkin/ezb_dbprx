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


@app.route( '/hello1/', methods=['GET'] )
def hi_a():
    """ Tests simple json response return. """
    return flask.jsonify( {'hello': 'world'} )


@app.route( '/hello2/', methods=['GET'] )
def hi_b():
    """ Tests logging. """
    log.info( u'hi there' )
    return flask.jsonify( {'hello': 'world2'} )


@app.route( '/basic_auth/', methods=['GET'] )
@basic_auth.required
def try_basic_auth():
    """ Tests basic-auth. """
    log.info( u'in proxy_app.try_basic_auth()' )
    return flask.jsonify( {'got': 'through'} )


@app.route( '/forbidden/', methods=['GET'] )
def try_forbidden():
    """ Tests forbidden response. """
    log.debug( u'in proxy_app.try_forbidden()' )
    return flask.abort( 403 )


@app.route( '/post_test/', methods=['POST'] )
def handle_post():
    """ Tests perceiving params response return. """
    value_a = flask.request.form['key_a'].strip()
    return flask.jsonify( {u'key_a': value_a} )


## real work ##


@app.route( u'/my_ip/', methods=['GET'] )
def show_ip():
    """ Returns ip.
        Note: this was a test, but could be useful for debugging. """
    ip = flask.request.remote_addr
    log.debug( u'in proxy_app.show_ip(); remote_addr, `%s`' % ip )
    return flask.jsonify( {u'client_ip': ip} )


@app.route( u'/search_new_request/', methods=['GET'] )
@basic_auth.required
def search():
    """ Searches for new requests. """
    client_ip = flask.request.remote_addr
    if not client_ip in settings.LEGIT_IPS.keys():
        log.debug( u'- in proxy_app.search_new_request(); client_ip `%s` not in LEGIT_IPS; returning forbidden' % client_ip )
        return flask.abort( 403 )
    db = db_handler.DB_Handler( log )
    result_list = db.search_new_request()
    return_dict = {
        u'request_type': u'search_new_request',
        u'datetime': unicode( datetime.datetime.now() ),
        u'result': result_list }
    return flask.jsonify( return_dict )


@app.route( u'/update_request_status/', methods=['POST'] )
@basic_auth.required
def update_request_status():
    """ Updates db request status. """
    log.debug( u'- in proxy_app.update_request_status(); starting' )
    client_ip = flask.request.remote_addr
    log.debug( u'- in proxy_app.update_request_status(); client_ip, `%s`' % client_ip )
    if not client_ip in settings.LEGIT_IPS.keys():
        log.debug( u'- in proxy_app.update_request_status(); returning forbidden' )
        return flask.abort( 403 )
    log.debug( u'- in proxy_app; update_request_status(); ip legit' )
    log.debug( u'- in proxy_app; update_request_status(); flask.request.form.keys(), %s' % sorted(flask.request.form.keys()) )
    db_id = flask.request.form[u'db_id']  # flask will return a '400 - Bad Request' if getting a value fails
    status = flask.request.form[u'status']
    try:
        assert status in [ u'in_process', u'processed' ]  # never changing it to its original 'not_yet_processed'
        assert db_id.isdigit()
    except Exception as e:
        log.error( u'- in proxy_app; update_request_status(); params grabbed; keys good but value(s) bad; db_id, `%s`; status, `%s`' % (db_id, status) )
        return flask.abort( 400, u'Bad data.' )
    log.debug( u'- in proxy_app; update_request_status(); params grabbed & data is valid' )
    db = db_handler.DB_Handler( log )
    result_dict = db.update_request_status( db_id, status )
    assert result_dict.keys() == [ u'status_update_result' ]
    return_dict = {
        u'request_type': u'update_request_status',
        u'db_id': db_id,
        u'requested_new_status': status,
        u'datetime': unicode( datetime.datetime.now() ),
        u'result': result_dict[ u'status_update_result' ]
        }
    return flask.jsonify( return_dict )


@app.route( u'/add_history_note/', methods=['POST'] )
@basic_auth.required
def add_history_note():
    """ Adds history note. """
    log.debug( u'- in proxy_app.add_history_note(); starting' )
    if not flask.request.remote_addr in settings.LEGIT_IPS.keys():
        log.debug( u'- in proxy_app.add_history_note(); returning forbidden for ip, `%s`' % flask.request.remote_addr )
        return flask.abort( 403 )
    ( db_id, history_note ) = ( flask.request.form[u'db_id'], flask.request.form[u'history_note'] )  # flask will return a '400 - Bad Request' if getting a value fails
    db = db_handler.DB_Handler( log )
    result_dict = db.update_history_note( db_id, history_note )
    return flask.abort( 403, u'Forbidden - under construction' )


if __name__ == '__main__':
    if os.getenv('DEVBOX') == 'true':
        app.run( host='0.0.0.0', debug=True )
    else:
        app.run()
