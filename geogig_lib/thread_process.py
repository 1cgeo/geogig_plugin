# -*- coding: utf-8 -*-
import threading
import time
exitFlag = 0

class Thread_Process(threading.Thread):
   def __init__(self, function, function_name, logger=False):
      threading.Thread.__init__(self)
      self.function = function
      self.function_name = function_name
      self.logger = logger

   def run(self):
      if exitFlag: 
            return
      self.logger.info(u"*STARTING {0}".format(self.function_name)) if self.logger else ''
      self.function()
      self.logger.info(u"#EXITING {0}".format(self.function_name)) if self.logger else ''
