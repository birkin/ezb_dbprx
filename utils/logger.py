# -*- coding: utf-8 -*-

""" Handles log setup. """

import logging, os


def setup_logger():
    """ Returns a logger to write to a file. """
    FILE_LOG_DIR = unicode( os.environ.get(u'ezb_dbprx__FILE_LOG_DIR') )
    FILE_LOG_LEVEL = unicode( os.environ.get(u'ezb_dbprx__FILE_LOG_LEVEL') )
    filename = u'%s/ezb_dbprx.log' % FILE_LOG_DIR
    formatter = logging.Formatter( u'[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s' )
    logger = logging.getLogger( u'ezb_dbprx' )
    level_dict = { u'debug': logging.DEBUG, u'info':logging.INFO }
    logger.setLevel( level_dict[FILE_LOG_LEVEL] )
    file_handler = logging.handlers.RotatingFileHandler( filename, maxBytes=(5*1024*1024), backupCount=1 )
    file_handler.setFormatter( formatter )
    logger.addHandler( file_handler )
    return logger
