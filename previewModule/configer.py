import os, sys, json


class configCreator(object):
    def __init__(self):
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


class configDefaults(object):
    def __init__(self):
        self.LOG = 'd:\\Dropbox\\FOX_renders\\log.json'
        self.SOURSE = 'd:\\Dropbox\\shotgunData\\FOX\\sequences\\Teaser_01_edit_01\\'
        self.COMPONENT = 'Anm'
        self.WORKPART = 'publish'
        self.PROGRAM = 'maya'
        self.PATH = 'd:\\Dropbox\\FOX_renders'
        self.XML_PROJECT = 'd:\\test.xml'
        self.STAMP_LOGO = 'd:\\Dropbox\\maya\\scripts\\previewModule\\images\\stampLogo.png'


