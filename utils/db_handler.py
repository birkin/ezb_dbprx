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
        self.file_logger.debug( u'in db_handler._setup_db_connection(); db_host, %s' % self.db_host )
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
        """ Returns dict with keys and values as unicode-strings.
            Called by execute_sql() """
        try:
            result_list = []
            for row_dict in dict_list:
                new_row_dict = {}
                for key,value in row_dict.items():
                    if type(value) == datetime.datetime:
                        value = unicode(value)
                    new_row_dict[ unicode(key) ] = unicode(value)
                result_list.append( new_row_dict )
            return result_list
        except Exception as e:
            message = u'in dev_code.db_handler._unicodify_resultset(); error: %s' % unicode( repr(e) )
            self.file_logger.error( message )

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

  # def search_new_request( self ):
  #   """ Returns json string of found request dict on find, 'result': 'not_found' on no-find.
  #       Called by: proxy_app.search() """
  #   return u'test_successful'

    def search_new_request( self ):
        """ Returns json string of found request dict on find, 'result': 'not_found' on no-find.
            Called by: proxy_app.search() """
        sql = settings.SEARCH_SQL
        self.file_logger.debug( u'in db_handler.search_new_request; sql, %s' % sql )
        dict_list = self.execute_sql( sql )
        return dict_list

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


# def get_db_handler( file_logger ):
#   db_handler = DB_Handler( file_logger=file_logger )
#   return db_handler


## helper functions

# def make_datetime_string():
#   """ Returns time-string like 'Wed Oct 23 14:49:38 EDT 2013'. """
#   import time
#   time_object = time.localtime(); assert type(time_object) == time.struct_time
#   time_string = time.strftime( u'%a %b %d %H:%M:%S %Z %Y', time_object )
#   return time_string

# def make_error_string():
#   """ Returns detailed error information for logging/debugging. """
#   error_message = u'error-type - %s; error-message - %s; line-number - %s' % (
#     sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2].tb_lineno, )
#   return error_message
