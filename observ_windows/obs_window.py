from collections import defaultdict
import psutil
import time
import datetime
import ast
from .proclist import ignoreporc

FILENAME = '.tempfile'
DATALIST = []

async def job():
    getprocs()

def getprocs():
    merged = defaultdict(lambda: {'cpu_percent': 0.0, 'memory_rss': 0})

    for proc in psutil.process_iter(attrs=['pid', 'name']):
        proc.cpu_percent(interval=None) 

    time.sleep(1)

    for proc in psutil.process_iter(attrs=['pid', 'name', 'cpu_percent', 'memory_info']):
        try:
            info = proc.info
            name = info['name']
            if name in ignoreporc: continue
            merged[name]['cpu_percent'] += info['cpu_percent']
            merged[name]['memory_rss'] += info['memory_info'].rss
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    mergelist = []
    for name, data in merged.items():
        if data['cpu_percent'] == 0: continue

        mergelist.append({'name': name, 'cpu': round(data['cpu_percent'],1), 'memory': round(data['memory_rss'] / 1024**2,1)})

    mergelist.sort(key=lambda x:x['cpu'], reverse=True)
    
    writedata(mergelist)

def readunsaveddata():
    print('unsaved data is: ')
    data = {}
    current_time = None
    with open(FILENAME, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line: continue

            if line.startswith("#"):   
                current_time = line[1:]
                data[current_time] = []
            else:
                data[current_time].append(ast.literal_eval(line))

    for key in data.keys():
        DATALIST.append([key,data[key]])

def writedata(data):
    now = datetime.datetime.now()
    DATALIST.append([now.strftime("#%Y%m%d%H%M"),data])
    with open(FILENAME, "a", encoding="utf-8") as f:
        
        f.write(now.strftime("#%Y%m%d%H%M\n"))

        for row in data:
            f.write(f"{row}\n")
    print('save data')

def getlist():
    return DATALIST



