#!/usr/bin/env python2.5

from asterisk.agi import *
from whitelistdb import WhitelistDB

class Runner(object):
    def __init__(self):
        self.agi = AGI()
        self.whitelistdb = WhitelistDB()
    
    def run(self):
        self.agi.verbose("InsidetheAGIscript.Woohoo!", 0)
        if self.whitelistdb.count(self.agi.env['agi_callerid']):
            self.agi.set_variable("ringthrough", 1)
        else:
            self.agi.set_variable("ringthrough", 0)
        self.agi.set_variable("results", self.whitelistdb.count(self.agi.env['agi_callerid']))

if __name__ == "__main__":
    x = Runner()
    x.run()
