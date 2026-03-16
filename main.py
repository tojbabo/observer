from observ_windows.obs_window import job, readunsaveddata
import asyncio
from sender.sender import sendjob, send2server

count = 0

async def sch():
    global count
    
    while True:
        await asyncio.sleep(60*10)
        count += 1

        if count == 6: 
            count = 0
            asyncio.create_task(sendjob())


        asyncio.create_task(job())
        print('do job')
    


if __name__ == "__main__":
    print('good')   
    readunsaveddata()
    send2server()
    # asyncio.run(sch())