#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""
Set all necessary variables to run the project
"""

import os, sys

class EnvManager(object):
   src_root = None
   config_dir = None
   config_file = None
   tools_dir = None

   def __init__(self):
      pre_file = os.path.realpath(__file__)
      pre_dir, f = os.path.split(pre_file)
      pre_dir, f = os.path.split(pre_dir)
      self.PJ_ROOT = os.path.abspath( pre_dir )
      self.PJ_CONFIG_DIR = self.PJ_ROOT + "/" + "Config"
      self.PJ_CONFIG_FILE = self.PJ_CONFIG_DIR + "/" + "settings.conf"
      self.PJ_TOOLS_DIR = self.PJ_ROOT + "/" + "Tools"
      self.PJ_LOGS_DIR = self.PJ_ROOT + "/" + "logs"

   def get_env_var(self, var):
      value = self.__dict__.get(var, None)
      if( value is not None ):
         # Uncomment the below print for debugging mode
         #print var[3:] , "=", value
         return value
      else:
         print "Environment Variable", var[3:] , "not set"
         return None

   def dump_all_vars(self):
      for k,v in self.__dict__.iteritems():
         print k,"=",v

# To Know the usage run the below
if __name__ == '__main__':
    u1 = EnvManager()
    u1.dump_all_vars()
