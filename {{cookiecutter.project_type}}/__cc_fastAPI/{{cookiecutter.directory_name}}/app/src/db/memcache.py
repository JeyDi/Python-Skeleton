"""
aiomcache example to cache in memory variables.
asyncio (PEP 3156) library to work with memcached.
- official documentation: https://pypi.org/project/aiomcache/
- implementation of functions: https://github.com/aio-libs/aiomcache/blob/master/aiomcache/client.py
- https://realpython.com/python-memcache-efficient-caching/

WARNING: remember to install memcached on your system
"""
import json
import asyncio
from aiomcache import Client
from aiomcache import exceptions as aiomexceptions


async def mem_connect(address: str = "localhost", port: int = 11211) -> any:
    try:
        mc = Client(host=address, port=port)
        # test if the server it's running
        await mc.version()
        return mc
    except aiomexceptions.ClientException:
        raise


async def mem_close(mc: object):
    await mc.close()
    return True


async def get_data(mc: object, key: str) -> str:
    value = await mc.get(key.encode())
    print(value)


async def multi_get_data():
    raise NotImplementedError


async def delete_data():
    raise NotImplementedError


async def set_data(mc: object, key: str, value: str, expire: int = None):
    result = await mc.set(key.encode(), value.encode(), exptime=expire or 0)
    return result


async def get_list_keys():
    raise NotImplementedError


async def mcache_flow(key: str, new_data: dict):

    # Create client connection
    mc = await mem_connect()

    # Get the data
    data = await get_data(mc, key)

    if data is not None:
        data = json.dump(data)
    # if there aren't data, create new one
    else:
        data = json.dumps(new_data)
        state = await set_data(mc, key, data)
        if state is True:
            data = json.dumps(state)

    return data


def test():
    key = "test"
    value = {"test1": "data1", "test2": 42, "test3": [1, 2, 3]}
    result = asyncio.run(mcache_flow(key, value))
    print(result)


if __name__ == "__main__":
    print("aiomcache example")
    test()
    print("finish")
