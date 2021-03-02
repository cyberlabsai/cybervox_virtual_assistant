import asyncio
import uvloop
import virtual_assistant.main as vta
if __name__=="__main__":
    uvloop.install()
    asyncio.run(vta.main())
