# -*- coding: utf-8 -*-
import sys, os, glob, json
from moviepy.editor import ImageClip, TextClip, CompositeVideoClip, ImageSequenceClip
from configer import configCreator, configDefaults


class sequenceProcessing(object):
    '''
    works with frames sequences
    '''
    def __init__(self):
        cc = configCreator()
        cd = configDefaults()
        for i in ['PATH', 'STAMP_LOGO']:
            if cc.getValue(i):
                setattr(self, i, cc.getValue(i))
            else:
                setattr(self, i, getattr(cd, i))

    def makeStamp(self, task_id):
        '''
        stamps all frames in specified sequence
        :param sequenceFolder: frames folder
        :param shotNumber: number to be stamped on each frame
        :return:
        '''
        tasksData = os.path.join(os.path.dirname(sys.argv[0]), 'config/renderData.json')
        tasks = json.load(open(tasksData))
        for task in tasks:
            if task['id'] == task_id:
                sequenceFolder = task['sequence_path']
                stampShotNumber = os.path.split(task['scene_path'])[-1].split('.')[0]
                stampShotVersion = os.path.split(task['scene_path'])[-1].split('.')[1]
                stampFocalLength = json.load(open(os.path.join(self.PATH, stampShotNumber, 'shotInfo.json')))['focalLength']
                frames = os.listdir(sequenceFolder)
                stampLogo = ImageClip(str(self.STAMP_LOGO), transparent=True)
                # for frame in frames:
                #     if os.path.splitext(frame)[-1] in ['.jpeg']:
                #         image = ImageClip(str(os.path.join(sequenceFolder, frame)))
                #         stampFrameNumber = frame.split('.')[1]
                #         txt_clip1 = TextClip(stampShotNumber, color='white', fontsize=20)
                #         txt_clip2 = TextClip('version: {}'.format(stampShotVersion[1:]), color='white', fontsize=15)
                #         txt_clip3 = TextClip('frame: {}'.format(stampFrameNumber), color='white', fontsize=15)
                #         txt_clip4 = TextClip('focalLength: {}'.format(stampFocalLength), color='white', fontsize=15)
                #         result = CompositeVideoClip([image, txt_clip1.set_position((5, 5)), txt_clip2.set_position((5, 25)), txt_clip3.set_position((5, 40)),
                #                                      txt_clip4.set_position((5, 55)), stampLogo.set_position(("left", "bottom"))])
                #         result.save_frame(os.path.join(sequenceFolder, frame))
                print 'STAMP#################'
                print stampShotNumber, stampShotVersion, stampFocalLength, self.STAMP_LOGO, self.PATH
                print '######################'

    def makeVideo(self, task_id):
        '''
        makes video file from specified frame folder
        :param sequenceFolder: frames folder
        :param shotNumber: number for naming the resulting video file
        :return:
        '''
        tasksData = os.path.join(os.path.dirname(sys.argv[0]), 'config/renderData.json')
        tasks = json.load(open(tasksData))
        for task in tasks:
            if task['id'] == task_id:
                sequenceFolder = task['sequence_path']
                sequenceFrames = glob.glob(os.path.join(sequenceFolder, '*.jpeg'))
                stampShotNumber = os.path.split(task['scene_path'])[-1].split('.')[0]
                # clip = ImageSequenceClip(sequenceFrames, fps=25)
                # if not os.path.exists(os.path.join(self.PATH, 'videos')):
                #     os.mkdir(os.path.join(self.PATH, 'videos'))
                # clip.write_videofile(os.path.join(self.PATH, 'mov', stampShotNumber+'.mp4'), fps=25)
                print 'VIDEO#################'
                print sequenceFolder, sequenceFrames[0], stampShotNumber, self.PATH
                print '######################'


class shotFinder(object):
    '''
    finds shots to be rendered
    '''
    def __init__(self):
        cc = configCreator()
        cd = configDefaults()
        for i in ['SOURSE', 'COMPONENT', 'WORKPART', 'APP']:
            if cc.getValue(i):
                setattr(self, i, cc.getValue(i))
            else:
                setattr(self, i, getattr(cd, i))

    def shotgunFolders(self):
        '''
        finds the latest version shots is shotgun folder structure
        :return: list of latest version shots
        '''
        shotList = []
        shotDirsList = glob.glob(self.SOURSE+'shot*')
        for shotDir in shotDirsList:
            for path, subdirs, files in os.walk(os.path.join(self.SOURSE, shotDir, self.COMPONENT, self.WORKPART, self.APP)):
                allShots = self.__filter(files)
                if allShots:
                    lastVersionShot = os.path.join(shotDir, self.COMPONENT, self.WORKPART, self.APP, allShots[-1])
                    shotList.append(lastVersionShot)
        return shotList

    def __filter(self, files):
        '''
        filters incoming files. They must be named properly.
        :param files: list of files to be checked
        :return: list of filtered shots
        '''
        shotList = []
        for file in files:
            if len(os.path.basename(file).split('.')) == 3:
                if len(os.path.basename(file).split('.')[1]) == 4 and os.path.basename(file).split('.')[1][0] == 'v':
                    if os.path.basename(file).split('.')[2] in ['ma', 'mb']:
                        shotList.append(file)
        return shotList

