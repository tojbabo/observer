import os
import sys
import asyncio

import common.logger as logger
from observ_windows.obs_window import job, readunsaveddata
from sender.sender import sendjob, send2server

VERSION = '0.0.3'

count = 0

LOCK_FILE = ".lock"

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

    if os.path.exists(LOCK_FILE):
        logger.error('process already running')

    else:

        with open(LOCK_FILE, 'w') as f:
            f.write(str(os.getpid()))
        try:    
            logger.info('windows observer start')
            readunsaveddata()
            send2server()
            asyncio.run(sch())
        finally:
            os.remove(LOCK_FILE)
    
    