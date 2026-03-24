import os
import psutil
import asyncio

import common.logger as logger
from observ_windows.obs_window import job, readunsaveddata
from sender.sender import sendjob, send2server
from __init__ import __version__

count = 0
LOCK_FILE = ".lock"
def is_already_running():
    if os.path.exists(LOCK_FILE):
        with open(LOCK_FILE, 'r') as f:
            pid = int(f.read().strip())
        
        # 해당 PID 프로세스가 실제로 살아있는지 확인
        if psutil.pid_exists(pid):
            logger.info(f"{pid} is already running")
            return True  # 진짜 실행 중
        else:
            os.remove(LOCK_FILE)  # 죽은 프로세스 lock이면 삭제
            logger.info(f"{pid} is deaded.. run program")
            return False
    return False

def create_lock():
    with open(LOCK_FILE, 'w') as f:
        f.write(str(os.getpid()))  # 현재 PID 저장


async def sch():
    global count
    
    while True:
        await asyncio.sleep(60*5)
        count += 1

        if count == 5: 
            count = 0
            asyncio.create_task(sendjob())

        asyncio.create_task(job())
    


if __name__ == "__main__":

    if is_already_running():
        pass

    else:
        create_lock()
        logger.info(f'windows observer start - {__version__}')
        readunsaveddata()
        send2server()
        asyncio.run(sch())
    
    