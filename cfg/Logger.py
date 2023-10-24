import logging

class Logger(object):

    def __init__(self, fname):
        logging.basicConfig(filename=fname,
                            filemode='a',
                            format='[%(asctime)s] %(name)s %(levelname)s : %(message)s',
                            datefmt='%d/%m/%Y %I:%M:%S %p',
                            level=logging.DEBUG)
        self.logger = logging
    
    def logDebug(self, msg):
        self.logger.debug(msg)
        
    def logInfo(self, msg):
        self.logger.info(msg)
    
    def logMTInfo(self, msg):
        self.mtLogger.info(msg)
        
    def logWarning(self, msg):
        self.logger.warning(msg)
        
    def logError(self,msg):
        self.logger.error(msg, exc_info=True)
        
    def logCritical(self, msg):
        self.logger.critical(msg)