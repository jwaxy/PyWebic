import asyncio
from pywebic import WebServer

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

srv = WebServer(loop=loop)

loop.run_until_complete(srv.run())
loop.close()