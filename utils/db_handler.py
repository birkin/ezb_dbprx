# -*- coding: utf-8 -*-

""" Handles db connection and executes sql. """

import datetime, json, os, pprint, random, sys
import MySQLdb
from ezb_dbprx.config import settings


class DB_Handler(object):

    def __init__(self, file_logger ):
        """ Sets up basics. """
        self.db_host = settings.DB_HOST
        self.db_port = settings.DB_PORT
        self.db_username = settings.DB_USERNAME
        self.db_password = settings.DB_PASSWORD
        self.db_name = settings.DB_NAME
        self.connection_object = None  # populated during queries
        self.cursor_object = None  # populated during queries
        self.file_logger = file_logger
        self.key_mapper = {  # converts database fields into more generic keys
            u'alt_edition': u'preference_alternate_edition',  # needed?
            u'barcode': u'patron_barcode',
            u'bibno': u'item_bib_number',  # needed?
            u'created': u'db_create_date',
            u'email': u'patron_email',
            u'eppn': u'patron_shib_eppn',
            u'firstname': u'patron_name_first',
            u'group': u'patron_shib_group',
            u'id': u'db_id',
            u'isbn': u'item_isbn',
            u'lastname': u'patron_name_last',
            u'loc': u'libary_location',  # needed?
            u'name': u'patron_name_firstlast',
            u'patronId': u'patron_id',  # needed?
            u'pref': u'preference_quick',  # needed?
            u'request_status': u'db_request_status',
            u'sfxurl': u'item_openurl',
            u'staffnote': u'staff_note',
            u'title': u'item_title',
            u'volumes': u'item_volumes',
            u'wc_accession': u'item_worldcat_id'
            }

    ## execute_sql() ##

    def execute_sql(self, sql):
        """ Executes sql; returns tuple of row-dicts.
            Example return data: ( {row1field1key: row1field1value, row1field2key: row1field2value}, {row2field1key: row2field1value, row2field2key: row2field2value} ) """
        try:
            self._setup_db_connection()
            if not self.cursor_object:
                return
            self.cursor_object.execute( sql )
            dict_list = self.cursor_object.fetchall()  # really a tuple of row-dicts
            dict_list = self._unicodify_resultset( dict_list )
            return dict_list
        except Exception as e:
            message = u'in dev_code.db_handler.execute_sql(); error: %s' % unicode( repr(e).decode(u'utf8', u'replace') )
            self.file_logger.error( message )
            return None
        finally:
            self._close_db_connection()

    def _setup_db_connection( self ):
        """ Sets up connection; populates instance attributes.
            Called by execute_sql() """
        self.file_logger.debug( u'in db_handler._setup_db_connection(); starting' )
        try:
            self.connection_object = MySQLdb.connect(
                host=self.db_host, port=self.db_port, user=self.db_username, passwd=self.db_password, db=self.db_name )
            self.file_logger.debug( u'in db_handler._setup_db_connection(); connection-object set' )
            self.cursor_object = self.connection_object.cursor(MySQLdb.cursors.DictCursor)
            return
        except Exception as e:
            message = u'in db_handler._setup_db_connection(); error: %s' % unicode( repr(e).decode(u'utf8', u'replace') )
            self.file_logger.error( message )

    def _unicodify_resultset( self, dict_list ):
        """ Takes tuple of row-dicts;
                Makes true list and ensures all keys and values are unicode;
                Returns list of type-corrected dicts.
            Called by execute_sql() """
        result_list = []
        for row_dict in dict_list:
            new_row_dict = {}
            for key,value in row_dict.items():
                if type(value) == datetime.datetime:
                    value = unicode(value)
                new_row_dict[ unicode(key) ] = unicode(value)
            result_list.append( new_row_dict )
        return result_list

    def _close_db_connection( self ):
        """ Closes db connection.
            Called by execute_sql() """
        try:
            self.cursor_object.close()
            self.connection_object.close()
            return
        except Exception as e:
            message = u'in dev_code.db_handler._close_db_connection(); error: %s' % unicode( repr(e).decode(u'utf8', u'replace') )
            self.file_logger.error( message )

    ## search_new_request() ##

    def search_new_request( self ):
        """ Returns json string of found request dict on find, 'result': 'not_found' on no-find.
            Called by: proxy_app.search_new_request() """
        sql = settings.SEARCH_SQL
        self.file_logger.debug( u'in db_handler.search_new_request; sql, %s' % sql )
        raw_dict_list = self.execute_sql( sql )
        self.file_logger.debug( u'in db_handler.search_new_request; raw_dict_list, %s' % raw_dict_list )
        if len( raw_dict_list ) > 0:
            massaged_dict = self._massage_raw_data( raw_dict_list )
            return massaged_dict
        else:
            return {}

    def _massage_raw_data( self, raw_dict_list ):
        """ Takes raw json list of a single dict representing db result;
                makes keys more generic;
                returns the generic dict (not a list).
            Called by search_new_request() .
            Possible TODO: add None to self.key_mapper if item isn't needed; test for that here and don't return it. """
        raw_dict = raw_dict_list[0]
        massaged_dict = {}
        for (key, value) in raw_dict.items():
            new_key = self.key_mapper[key]
            massaged_dict[new_key] = value
        return massaged_dict

    ## other ##

    def jsonify_db_data( self, data_dict ):
        """ Returns json string for given tuple of row-dict entries.
            Allows result to be logged easily.
            Called by ezb_controller.py """
        data_dict[u'created'] = unicode( data_dict[u'created'] )
        jstring = json.dumps( data_dict, sort_keys=True, indent=2 )
        return jstring

    def update_request_status( self, row_id, status ):
        """ Updates request table status field.
            Called by ezb_controller.py """
        sql = u"UPDATE `aaa` SET bbb = '%s' WHERE id = %s" % ( status, row_id )
        result = self.execute_sql( sql )
        self.file_logger.debug( u'in dev_code.db_handler.update_request_status(); status updated to %s' % status )
        return

    def update_history_note( self, request_id, note ):
        """ Updates history table note field.
            Called by ezb_controller.py """
        sql = u"INSERT INTO `aaa` ( field_a, field_b ) VALUES ( '%s', '%s' )" % ( request_id, note )
        result = self.execute_sql( sql )
        self.file_logger.debug( u'- in dev_ezb_controller.py; uc.DB_Handler.update_history_note(); note updated' )
        return

  # end class DB_Handler()

