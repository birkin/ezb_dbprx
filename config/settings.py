# -*- coding: utf-8 -*-

import json, os


## db access
DB_HOST = unicode( os.environ.get(u'ezb_dbprx__DB_HOST') )
DB_PORT = int( unicode(os.environ.get(u'ezb_dbprx__DB_PORT')) )
DB_USERNAME = unicode( os.environ.get( u'ezb_dbprx__DB_USERNAME') )
DB_PASSWORD = unicode( os.environ.get(u'ezb_dbprx__DB_PASSWORD') )
DB_NAME = unicode( os.environ.get( u'ezb_dbprx__DB_NAME') )

## db sql
SEARCH_SQL = unicode( os.environ.get( u'ezb_dbprx__SEARCH_SQL') )  # for db_handler.DB_Handler.search_new_request()
UPDATE_REQUEST_STATUS_SQL_PATTERN = unicode( os.environ.get( u'ezb_dbprx__UPDATE_REQUEST_STATUS_SQL_PATTERN') )  # for db_handler.DB_Handler.update_request_status()
CONFIRM_REQUEST_STATUS_SQL_PATTERN = unicode( os.environ.get( u'ezb_dbprx__CONFIRM_REQUEST_STATUS_SQL_PATTERN') )  # for db_handler.DB_Handler.update_request_status()

## file-logger
LOG_DIR = unicode( os.environ.get(u'ezb_dbprx__LOG_DIR') )
LOG_LEVEL = unicode( os.environ.get(u'ezb_dbprx__LOG_LEVEL') )

## basic auth
BASIC_AUTH_USERNAME = unicode( os.environ.get(u'ezb_dbprx__BASIC_AUTH_USERNAME') )
BASIC_AUTH_PASSWORD = unicode( os.environ.get(u'ezb_dbprx__BASIC_AUTH_PASSWORD') )

## other
LEGIT_IPS = json.loads( unicode(os.environ.get(u'ezb_dbprx__LEGIT_IPS')) )

# end
