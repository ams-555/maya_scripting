# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
from multiprocessing import Process, Pipe
import json


app = Flask(__name__)


def fake_launch(conn, jtasks):
    tasks = json.loads(jtasks)
    for task in tasks:
        task['done'] = 1     # sets 1 for every 'done' key
    conn.send(json.dumps(tasks))
    conn.close()


@app.route('/task', methods=['POST'])  # we send [{"id":1, "done":0}, {"id":2,"done":0}]
def modify_task():
    if request.method == 'POST':
        parent_conn, child_conn = Pipe()
        jtasks = json.dumps(request.json)
        p = Process(target=fake_launch, args=(child_conn, jtasks))
        p.start()
        result = parent_conn.recv()
        return result   # we get [{"id":1, "done":1}, {"id":2,"done":1}]


if __name__ == '__main__':
    app.run(debug=True)

# curl -i -H "Content-Type: application/json" -X POST -d "[{"""id""":1, """done""":0},
#                                                           {"""id""":2,"""done""":0}]' http://127.0.0.1:5000/task

