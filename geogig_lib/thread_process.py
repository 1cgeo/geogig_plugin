# -*- coding: utf-8 -*-
import threading
import time

exitFlag = 0

class Thread_Process(threading.Thread):
   def __init__(self, function, function_name):
      threading.Thread.__init__(self)
      self.function = function
      self.function_name = function_name

   def run(self):
      if exitFlag:
            return
      print "*STARTING {0}\n".format(self.function_name)
      self.function()
      print "#EXITING {0}\n".format(self.function_name)
