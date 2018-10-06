# -*- coding: utf-8 -*-
import threading
import time
exitFlag = 0

class Thread_Process(threading.Thread):
   def __init__(self, function):
      threading.Thread.__init__(self)
      self.function = function

   def run(self):
      if exitFlag: 
            return
      self.function()
