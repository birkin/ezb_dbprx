# -*- coding: utf-8 -*-

import os


# db access
DB_HOST = unicode( os.environ.get(u'ezb_dbprx__DB_HOST') )
DB_PORT = int( unicode(os.environ.get(u'ezb_dbprx__DB_PORT')) )
DB_USERNAME = unicode( os.environ.get( u'ezb_dbprx__DB_USERNAME') )
DB_PASSWORD = unicode( os.environ.get(u'ezb_dbprx__DB_PASSWORD') )
DB_NAME = unicode( os.environ.get( u'ezb_dbprx__DB_NAME') )
SEARCH_SQL = unicode( os.environ.get( u'ezb_dbprx_SEARCH_SQL') )

# file-logger
LOG_DIR = unicode( os.environ.get(u'ezb_dbprx__LOG_DIR') )
LOG_LEVEL = unicode( os.environ.get(u'ezb_dbprx__LOG_LEVEL') )

# basic auth
BASIC_AUTH_USERNAME = unicode( os.environ.get(u'ezb_dbprx__BASIC_AUTH_USERNAME') )
BASIC_AUTH_PASSWORD = unicode( os.environ.get(u'ezb_dbprx__BASIC_AUTH_PASSWORD') )

# end
