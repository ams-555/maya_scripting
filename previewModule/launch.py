import sys, os
# from program import sequenceProcessing
from configer import configCreator, configDefaults
from renderData import renderDataHolder
from program import sequenceProcessing
import time

class renderLauncher(object):
    '''
    read the user command line flags, apply them, and run render itself
    '''
    def __init__(self):
        cc = configCreator()
        cd = configDefaults()
        for i in ['PATH']:
            if cc.getValue(i):
                setattr(self, i, cc.getValue(i))
            else:
                setattr(self, i, getattr(cd, i))

    def run(self):
        r = renderDataHolder()
        s = sequenceProcessing()
        if r.getAllRenderable():
            for shot in r.getAllRenderable():
                r.setStatus(shot['id'], 0)   # inProgress
                result = self.__doRender(shot['scene_path'], shot['sequence_path'])
                s.makeStamp(shot['id'])
                # s.makeVideo(shot['id'])
                r.setStatus(shot['id'], 1)   # done
                r.setOutput(shot['id'], result)
            return True
        else:
            return False

    # def __doRender(self, shot, imagePath):
    #     '''
    #     run render itself
    #     :param shot: shot to be rendered
    #     :param imagePath: output folder
    #     :return:
    #     '''
    #     print '>>> render shot: ', shot, imagePath
    #     p = subprocess.Popen(['Render', '-cam', 'shotCam', '-preRender', 'python("import previewRenderSetup")', '-rd', imagePath, shot],
    #                             stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    #     (output, err) = p.communicate()
    #     print output, err
    #     return output

    def __doRender(self, shot, sequence_path):
        print 'RENDER#################'
        print '>>> maya: render complete ', shot, '\n>>> images ', sequence_path
        print '######################'
        return 'I am maya output info'
