import os, sys, json


class configCreator(object):
    def __init__(self):
        print '__init__ congig creator'
        self.root = os.path.join(os.path.dirname(sys.argv[0]), 'config')
        if not os.path.exists(self.root):
            os.mkdir(self.root)
            print 'mkdir'
        if not os.path.exists(os.path.join(self.root, 'config.json')):
            json.dump({}, open(os.path.join(self.root, 'config.json'), 'w'))
            print 'make config.json'


    def getValue(self, logKey):
        if logKey in json.load(open(os.path.join(self.root, 'config.json'))).keys():
            logValue = json.load(open(os.path.join(self.root, 'config.json')))[logKey]
            return logValue
        else:
            return None

