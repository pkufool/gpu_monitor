# Copyright 2021 pkufool. All Rights Reserved.
# Author: wkang@pku.org.cn

import codecs
import json
import os
import subprocess as sp
import sys

from flask import Flask, request, render_template
import yaml

app = Flask(__name__)
pwd = os.path.dirname(__file__)

servers = {}
config = yaml.load(codecs.open(os.path.join(pwd, "./config.yaml"),
                               encoding='utf-8'),
                   Loader=yaml.FullLoader)
for it in config['servers']:
    servers[it['ip']] = it


def get_stats(server):
    user = server['user']
    ip = server['ip']
    name = server['name']
    cmd = "ssh -o StrictHostKeyChecking=no -t {}@{} nvidia-smi --query-gpu=index,name,memory.used,"\
          "memory.total,utilization.gpu --format=csv,noheader,nounits"\
          .format(user, ip)
    proc = sp.Popen(cmd.strip().split(), stdout=sp.PIPE, stderr=sp.PIPE)
    stdout, stderr = proc.communicate()
    stats = []
    for line in stdout.decode('utf-8').strip().split("\n"):
        toks = [x.strip() for x in line.strip().split(",")]
        stats.append({
            'index': int(toks[0]),
            'name': toks[1],
            'memory_used': int(toks[2]),
            'memory_total': int(toks[3]),
            'utilization_gpu': int(toks[4])
        })
    return {'server': name, 'ip': ip, 'gpus': stats}


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/machines', methods=['GET'])
def machines():
    config = yaml.load(codecs.open(os.path.join(pwd, "./config.yaml"),
                                   encoding='utf-8'),
                       Loader=yaml.FullLoader)
    for it in config['servers']:
        servers[it['ip']] = it
    return json.dumps(list(servers.keys()), ensure_ascii=False)


@app.route('/stats', methods=['GET'])
def stats():
    ip = request.args.get("ip")
    stats = get_stats(servers[ip])
    return json.dumps({"data": stats}, ensure_ascii=False)
