# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify, abort
from multiprocessing import Process, Pipe
from renderData import renderDataHolder
from launch import renderLauncher
import json

app = Flask(__name__)

def renderProcess():
    l = renderLauncher()
    l.run()

@app.route('/render')
def run():
    p = Process(target=renderProcess)
    p.start()
    return jsonify({'render started': True})

@app.route('/tasks/scan', methods=['GET'])
def scanTasks():
    if request.method == 'GET':
        r = renderDataHolder()
        result = r.scanShotgunFolders()
        return jsonify({'shotgunFoldersScan': result})

@app.route('/tasks', methods=['POST'])
def addTask():
    if request.method == 'POST':
        r = renderDataHolder()
        task_id = r.addNewTask(request.json.get('scene_path'), request.json.get('sequence_path'))
        return jsonify({'id': task_id}), 201

@app.route('/tasks/<int:task_id>', methods=['GET'])
def readStatus(task_id):
    if request.method == 'GET':
        r = renderDataHolder()
        status = r.getValue(task_id, 'status')
        output = r.getValue(task_id, 'output')
        if status or output:
            return jsonify({'status': status, 'output': output})
        else:
            abort(404)

@app.route('/tasks', methods=['GET'])
def getTasks():
    if request.method == 'GET':
        r = renderDataHolder()
        all_tasks = r.getAllTasks()
        return jsonify({'all_tasks': all_tasks})

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def deleteTask(task_id):
    if request.method == 'DELETE':
        r = renderDataHolder()
        result = r.deleteTask(task_id)
        return jsonify({'result': result}), 301


if __name__ == '__main__':
    app.run(debug=True)



# curl -H "Content-Type: application/json" -d "{"""path""":"""path/to/images"""}" http://127.0.0.1:5000/tasks