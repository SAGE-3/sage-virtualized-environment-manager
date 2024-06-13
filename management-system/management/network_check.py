import pycurl
import websockets
import asyncio
from io import BytesIO

class NetworkCheck:
    @staticmethod
    async def wait_for_url(url):
        tasks = []
        task = asyncio.get_event_loop().run_in_executor(None, NetworkCheck.__website_online__, url, 1)
        tasks.append(task)
        statuses = await asyncio.gather(*tasks)
        return any(statuses)

    @staticmethod
    def __website_online__(url, timeout=1):
        buffer = BytesIO()
        c = pycurl.Curl()
        c.setopt(c.URL, url)
        c.setopt(c.WRITEDATA, buffer)
        c.setopt(c.TIMEOUT, timeout)

        try:
            c.perform()
            status_code = c.getinfo(c.RESPONSE_CODE)
            print(f"{url} is up and running!")
            return True
        except pycurl.error as e:
            print(f"{url} is down. Error: {e}")
            return False
        finally:
            c.close()

    @staticmethod
    async def check_websocket_connection(url):
        try:
            async with websockets.connect(url) as ws:
                return True
        except:
            return False


