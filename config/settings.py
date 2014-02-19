# -*- coding: utf-8 -*-

import os


# db access
DB_HOST = unicode( os.environ.get(u'ezb_dbprx__DB_HOST') )
DB_PORT = int( unicode(os.environ.get(u'ezb_dbprx__DB_PORT')) )
DB_USERNAME = unicode( os.environ.get( u'ezb_dbprx__DB_USERNAME') )
DB_PASSWORD = unicode( os.environ.get(u'ezb_ctl__DB_PASSWORD') )
DB_NAME = unicode( os.environ.get( u'ezb_dbprx__DB_NAME') )

# file-logger
FILE_LOG_DIR = unicode( os.environ.get(u'ezb_dbprx__FILE_LOG_DIR') )
FILE_LOG_LEVEL = unicode( os.environ.get(u'ezb_dbprx__FILE_LOG_LEVEL') )
