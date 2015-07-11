# -*- coding: utf-8 -*-
import os
import glob
import json
from moviepy.editor import ImageClip, TextClip, CompositeVideoClip, ImageSequenceClip


class sequenceProcessing(object):
    '''
    works with rendered frame sequences
    '''
    def __init__(self):
        self.PATH = json.load(open(r'd:\Dropbox\maya\scripts\previewModule\config\config.json'))['PATH']
        self.STAMP_LOGO = json.load(open(r'd:\Dropbox\maya\scripts\previewModule\config\config.json'))['STAMP_LOGO']
        self.LOG = json.load(open(r'd:\Dropbox\maya\scripts\previewModule\config\config.json'))['LOG']

    def makeStamp(self, sequenceFolder, shotNumber):
        '''
        stamps all frames in specified sequence
        :param sequenceFolder: frames folder
        :param shotNumber: number to be stamped on each frame
        :return:
        '''
        frames = os.listdir(sequenceFolder)
        stampLogo = ImageClip(str(self.STAMP_LOGO), transparent=True)
        for frame in frames:
            if os.path.splitext(frame)[-1] in ['.jpeg']:
                image = ImageClip(str(os.path.join(sequenceFolder, frame)))
                stampFocalLength = json.load(open(os.path.join(self.PATH, shotNumber, 'shotInfo.json')))['focalLength']
                stampShotNumber = json.load(open(os.path.join(self.PATH, shotNumber, 'shotInfo.json')))['shotNumber']
                stampShotVersion = json.load(open(self.LOG))[shotNumber]
                stampFrameNumber = frame.split('.')[1]
                txt_clip1 = TextClip(stampShotNumber, color='white', fontsize=20)
                txt_clip2 = TextClip('version: {}'.format(stampShotVersion[1:]), color='white', fontsize=15)
                txt_clip3 = TextClip('frame: {}'.format(stampFrameNumber), color='white', fontsize=15)
                txt_clip4 = TextClip('focalLength: {}'.format(stampFocalLength), color='white', fontsize=15)
                result = CompositeVideoClip([image, txt_clip1.set_position((5, 5)), txt_clip2.set_position((5, 25)), txt_clip3.set_position((5, 40)),
                                             txt_clip4.set_position((5, 55)), stampLogo.set_position(("left", "bottom"))])
                result.save_frame(os.path.join(sequenceFolder, frame))
            else:
                pass

    def makeVideo(self, sequenceFolder, shotNumber):
        '''
        makes video file from specified frame folder
        :param sequenceFolder: frames folder
        :param shotNumber: number for naming the resulting video file
        :return:
        '''
        frameSequence = glob.glob(os.path.join(sequenceFolder, '*.jpeg'))
        clip = ImageSequenceClip(frameSequence, fps=25)
        if not os.path.exists(os.path.join(self.PATH, 'mov')):
            os.mkdir(os.path.join(self.PATH, 'mov'))
        clip.write_videofile(os.path.join(self.PATH, 'mov', shotNumber+'.mp4'), fps=25)


class logProcessing(object):
    '''
    creates a new log file, if there were no such file, and updates log file data.
    '''
    def __init__(self):
        self.LOG = str(json.load(open(r'd:\Dropbox\maya\scripts\previewModule\config\config.json'))['LOG'])
        if not os.path.exists(self.LOG):
            # create an empty log
            dict = {}
            json.dump(dict, open(self.LOG, 'w'), indent=4)
        self.currentData = json.load(open(self.LOG))

    def __logReader(self, shotNumber):
        '''
        reads the version of the specified shot from the log file.
        :param shotNumber: number of the shot to be read.
        :return: shot version or None if there were no data about this shot in log file
        '''
        if shotNumber in self.currentData.keys():
            return self.currentData[shotNumber]
        else:
            return None

    def logWriter(self, shotNumber, shotVersion):
        '''
        Updates log file data. Writes the latest version of the current shot.
        :param shotNumber: current shot number to be writen to the log file
        :param shotVersion: current shot version to be writen to the log file
        :return:
        '''
        self.currentData[shotNumber] = shotVersion
        json.dump(self.currentData, open(self.LOG, 'w'), indent=4)

    def compare(self, argFile=None, argFolder=None):
        '''
        Compares versions of incoming shots and versions from log file
        :param argFile: shot provided by the user from the command line
        :param argFolder: folder provided by the user from the command line
        :return: list of shots to be rendered
        '''
        s = shotFinder()
        shotsForRender = []
        if argFolder:
            shots = s.customFolder(argFolder)
        elif argFile:
            shots = s.customFile(argFile)
        else:
            shots = s.shotgunFolders()
        for shot in shots:
            shotNumber = os.path.basename(shot).split('.')[0]
            shotVersion = os.path.basename(shot).split('.')[1]
            if shotVersion > self.__logReader(shotNumber):
                shotsForRender.append(shot)
        return shotsForRender


class shotFinder(object):
    '''
    finds shots to be rendered
    '''
    def __init__(self, argFile=None, argFolder=None):
        self.SOURSE = json.load(open(r'd:\Dropbox\maya\scripts\previewModule\config\config.json'))['SOURSE']
        self.COMPONENT = json.load(open(r'd:\Dropbox\maya\scripts\previewModule\config\config.json'))['COMPONENT']
        self.WORKPART = json.load(open(r'd:\Dropbox\maya\scripts\previewModule\config\config.json'))['WORKPART']
        self.PROGRAM = json.load(open(r'd:\Dropbox\maya\scripts\previewModule\config\config.json'))['PROGRAM']

    def shotgunFolders(self):
        '''
        finds the latest version shot is shotgun folder structure
        :return: list of latest shots
        '''
        shotList = []
        shotDirsList = glob.glob(self.SOURSE+'shot*')
        for shotDir in shotDirsList:
            pipelineSteps = os.listdir(shotDir)
            for pipelineStep in pipelineSteps:
                if pipelineStep == self.COMPONENT:
                    stepStages = os.listdir(os.path.join(shotDir, self.COMPONENT))
                    for stage in stepStages:
                        if stage == self.WORKPART:
                            allFiles = os.listdir(os.path.join(shotDir, self.COMPONENT, self.WORKPART, self.PROGRAM))
                            if allFiles:
                                lastFile = glob.glob(os.path.join(shotDir, self.COMPONENT, self.WORKPART, self.PROGRAM)+'\Shot*.v*')
                                if lastFile != []:
                                    shot = lastFile[-1]
                                    shotList.append(shot)
        return shotList

    def customFolder(self, argFolder):
        '''
        finds shots in folder provided by the user from the command line
        :param argFolder: folder provided by the user from the command line
        :return: list of shots that mach naming rools
        '''
        allFiles = glob.glob(argFolder+'\*')
        return self.__filter(allFiles)

    def customFile(self, argFile):
        '''
        :param argFile: file provided by the user from the command line
        :return: file if it maches naming rools
        '''
        return self.__filter(argFile)

    def __filter(self, files):
        '''
        filters incoming files. They must be named properly.
        :param files: list of foles to be checked
        :return: list of filtered shots
        '''
        shotList = []
        for file in files:
            if len(os.path.basename(file).split('.')) == 3:
                if len(os.path.basename(file).split('.')[1]) == 4 and os.path.basename(file).split('.')[1][0] == 'v':
                    if os.path.basename(file).split('.')[2] in ['ma', 'mb']:
                        shotList.append(file)
        return shotList

