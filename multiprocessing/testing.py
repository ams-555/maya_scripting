# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
from multiprocessing import Process, Pipe
import json

app = Flask(__name__)


def fake_launch(conn, jtasks):
    tasks = json.loads(jtasks)
    for task in tasks:
        task['done'] = 1
    conn.send(json.dumps(tasks))
    conn.close()


@app.route('/task', methods=['POST'])
def modify_task():
    if request.method == 'POST':
        parent_conn, child_conn = Pipe()
        jtasks = json.dumps(request.json)
        p = Process(target=fake_launch, args=(child_conn, jtasks))
        p.start()
        result = parent_conn.recv()
        return result


if __name__ == '__main__':
    app.run(debug=True)

