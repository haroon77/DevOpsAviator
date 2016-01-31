#!/usr/bin/env python

import sys
from string import Template

from ConfigParser import SafeConfigParser

from EnvManager import EnvManager

class UtilsManager(object):
    config_parser = None
    config_file = None

    def __init__(self):
        self.config_file = EnvManager().get_env_var("PJ_CONFIG_FILE")
        self.config_parser = SafeConfigParser()
        if (self.config_file is not None):
            try:
                self.config_parser.read(self.config_file)
            except Exception as err:
                print "Unable to read config file"

    def get_config_file(self):
        return (self.config_file)

    def get_config_parser(self):
        return (self.config_parser)

    def get_settings(self, section):
        settings = {}
        pj_root = EnvManager().get_env_var("PJ_ROOT")
        try:
            attribs = self.config_parser.items(section)
            for name, attrib in attribs:
                if "PROJECT_ROOT" in attrib:
                    attrib = Template(attrib).substitute(PROJECT_ROOT=pj_root)
                settings[name] = attrib
        except Exception as e:
            print "Error while parsing config file", e.args
            return False
        return settings

if __name__ == '__main__':
    ut = UtilsManager().get_settings('main')
    if sys.flags.debug:
        print "Main Config: ", ut
