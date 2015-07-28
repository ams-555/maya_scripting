# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
from multiprocessing import Process, Pipe
from renderData import renderDataHolder
from launch import renderLauncher
import json

app = Flask(__name__)

def renderProcess(conn):
    l = renderLauncher()
    result = l.run()
    conn.send(result)
    conn.close()

@app.route('/render')
def run():
    parent_conn, child_conn = Pipe()
    p = Process(target=renderProcess, args=(child_conn,))
    p.start()
    result = parent_conn.recv()
    return jsonify({'render started': result})

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
        task_id = r.addNewTask(request.json.get('path'))
        return jsonify({'id': task_id})

@app.route('/tasks/<int:task_id>', methods=['GET'])
def readStatus(task_id):
    if request.method == 'GET':
        r = renderDataHolder()
        taskStatus = r.getStatus(task_id)
        return jsonify({'status': taskStatus})

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
        return jsonify({'result': result})


if __name__ == '__main__':
    app.run(debug=True)

# curl -i -H "Content-Type: application/json" -X POST -d "[{"""id""":1, """done""":0},
#                                                           {"""id""":2,"""done""":0}]' http://127.0.0.1:5000/tasks


