import sys, os
# from program import sequenceProcessing
from configer import configCreator, configDefaults
from renderData import renderDataHolder
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
        if r.getAllRenderable():
            for shot in r.getAllRenderable():
                r.editStatus(shot['id'], 0)   # inProgress
                self.__doRender(shot['path'], 'path/to/image/folder')
                r.editStatus(shot['id'], 1)   # done
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

    def __doRender(self, shot, imagePath):
        time.sleep(5)
        print '>>> maya: render complete ', shot, '\n>>> images ', imagePath


