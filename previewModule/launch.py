import sys
import os
import argparse
import subprocess
from program import logProcessing, shotFinder, sequenceProcessing
import json

def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--shot', default=None)
    parser.add_argument('-f', '--folder', default=None)
    parser.add_argument('-ra', '--renderall', action='store_true', default=False)
    parser.add_argument('-nv', '--novideo', action='store_true', default=False)
    parser.add_argument('-ns', '--nostamp', action='store_true', default=False)
    return parser

parser = createParser()
namespace = parser.parse_args()


class renderLauncher(object):
    '''
    read the user command line flags, apply them, and run render itself
    '''
    def __init__(self):
        self.PATH = json.load(open(r'd:\Dropbox\maya\scripts\previewModule\config\config.json'))['PATH']
        self.inputFile = namespace.shot
        self.inputFolder = namespace.folder
        self.renderall = namespace.renderall
        self.novideo = namespace.novideo
        self.nostamp = namespace.nostamp
        self.launcher()

    def whatToRender(self):
        '''
        depending on -ra flag skip or not log search
        :return: list of shots to be rendered
        '''
        if self.renderall:
            s = shotFinder()
            if self.inputFile:
                shotsForRender = s.customFile(self.inputFile)
            elif self.inputFolder:
                shotsForRender = s.customFolder(self.inputFolder)
            else:
                shotsForRender = s.shotgunFolders()
            return shotsForRender
        else:
            l = logProcessing()
            shotsForRender = l.compare(argFile=self.inputFile, argFolder=self.inputFolder)
            return shotsForRender

    def launcher(self):
        '''
        launches all functions one by one for each shot that has to be rendered
        :return:
        '''
        for shot in self.whatToRender():
            s = sequenceProcessing()
            l = logProcessing()
            imagePath = os.path.join(self.PATH, os.path.basename(shot).split('.')[0])
            shotNumber = os.path.basename(shot).split('.')[0]
            shotVersion = os.path.basename(shot).split('.')[1]
            self.__doRender(shot, imagePath)
            l.logWriter(shotNumber, shotVersion)
            if not self.nostamp:
                s.makeStamp(imagePath, shotNumber)
            if not self.novideo:
                s.makeVideo(str(imagePath), str(shotNumber))

    def __doRender(self, shot, imagePath):
        '''
        run render itself
        :param shot: shot to be rendered
        :param imagePath: output folder
        :return:
        '''
        p = subprocess.Popen(['Render', '-cam', 'shotCam', '-preRender', 'python("import previewRenderSetup")', '-rd', imagePath, shot],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        (output, err) = p.communicate()
        print output, err


renderLauncher()