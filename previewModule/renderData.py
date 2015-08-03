import os, sys, json
from program import shotFinder
from configer import configCreator, configDefaults


class renderDataHolder(object):
    def __init__(self):
        cc = configCreator()
        cd = configDefaults()
        for i in ['PATH']:
            if cc.getValue(i):
                setattr(self, i, cc.getValue(i))
            else:
                setattr(self, i, getattr(cd, i))
        self.root = os.path.join(os.path.dirname(sys.argv[0]), 'config')
        if not os.path.exists(self.root):
            os.mkdir(self.root)
        self.renderDataFile = os.path.join(self.root, 'renderData.json')
        if not os.path.exists(self.renderDataFile):
            renderData = []
            json.dump(renderData, open(self.renderDataFile, 'w'), indent=4)
        self.tasks = json.load(open(self.renderDataFile))

    def addNewTask(self, pathToScene, pathToSequence):
        newTask = {}
        newTask['id'] = self.__maxID()+1
        newTask['scene_path'] = pathToScene
        newTask['status'] = -1
        newTask['sequence_path'] = pathToSequence
        newTask['output'] = 'not rendered yet'
        self.tasks.append(newTask)
        json.dump(self.tasks, open(self.renderDataFile, 'w'), indent=4)
        return newTask['id']

    def getValue(self, task_id, key):
        if self.__isID(task_id):
            for task in self.tasks:
                if task['id'] == task_id:
                    return task[key]
        else:
            return False

    def deleteTask(self, task_id):
        if self.__isID(task_id):
            for task in self.tasks:
                if task['id'] == task_id:
                    self.tasks.remove(task)
                    json.dump(self.tasks, open(self.renderDataFile, 'w'), indent=4)
                    return True
        else:
            return False

    def setStatus(self, task_id, status):  # add ID check
        for task in self.tasks:
            if task['id'] == task_id:
                task['status'] = status
        json.dump(self.tasks, open(self.renderDataFile, 'w'), indent=4)

    def setOutput(self, task_id, output):  # add ID check
        for task in self.tasks:
            if task['id'] == task_id:
                task['output'] = output
        json.dump(self.tasks, open(self.renderDataFile, 'w'), indent=4)

    def getAllTasks(self):
        return self.tasks

    def getAllRenderable(self):
        allRenderable = []
        for task in self.tasks:
            if task['status'] == -1:
                allRenderable.append(task)
        return allRenderable

    def scanShotgunFolders(self):
        s = shotFinder()
        shotList = s.shotgunFolders()
        for shot in shotList:
            self.__cleaner(shot)
            sequence_path = os.path.join(self.PATH, os.path.basename(shot).split('.')[0])
            self.addNewTask(shot, sequence_path)  # fix
        return True

    def __maxID(self):
        if self.tasks:
            IDs = []
            for task in self.tasks:
                IDs.append(task['id'])
            return sorted(IDs)[-1]
        else:
            return 0

    def __isID(self, task_id):
        if self.tasks:
            IDs = []
            for task in self.tasks:
                IDs.append(task['id'])
            if task_id in IDs:
                return True
            else:
                return False

    def __cleaner(self, incomingShot):
        if self.tasks:
            for task in self.tasks:
                if task['scene_path'] == incomingShot and task['status'] == -1:
                    self.tasks.remove(task)
            json.dump(self.tasks, open(self.renderDataFile, 'w'), indent=4)



