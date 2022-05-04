import json
import asyncio
import aioredis as ars
from datetime import timedelta


async def redis_connect(
    port: str = 6362, username: str = "default", password: str = None
):
    try:
        conn = await ars.from_url(
            f"redis://localhost:{port}",
            encoding="utf-8",
            db=0,
            username=username,
            password=password,
            decode_responses=True,
        )
        # val = await conn.execute('GET', 'my-key')
        ping = await conn.ping()
        if ping is True:
            return conn
        else:
            raise ars.ConnectionError
    except ars.AuthenticationError as message:
        print(f"Redis auth error: {message}")
        raise ars.AuthenticationError


async def redis_close(conn: ars.Connection) -> bool:
    # gracefully closing underlying connection
    try:
        if await conn.ping():
            await conn.close()
            return True
        else:
            return False
    except ars.ResponseError as message:
        raise Exception(f"Impossible to close the connection, because: {message}")


async def get_data(client: ars.Connection, key: str) -> str:
    try:
        val = await client.get(key)
        # val = client.get(key)
        return val
    except ars.ResponseError as message:
        raise Exception(
            f"Impossible to get the data with key: {key}, because: {message}"
        )


async def get_list_keys(client: ars.Connection = None, pattern: str = "*") -> list:
    try:
        if not client:
            # Get the client
            client = await redis_connect()

        keys = await client.keys(pattern)
        return keys
    except ars.ResponseError as message:
        raise Exception(
            f"Impossible to get the list of keys with pattern: {pattern}, because: {message}"
        )


async def clear_data(
    key: str, direct: bool = True, namespace: str = None, client: ars.Connection = None
) -> bool:
    """Clear and delete cache data from redis database.

    This function work in 2 different ways:
    1. If direct is True, it will delete the key directly from redis database.
    2. If direct is False, it will delete the key from redis database using a lua script composed with key and namespace. Be carefull because with direct = False you can delete all the keys that match the lua expression built.

    Args:
        key (str): the key of the data you want to delete
        direct (bool, optional): If you want to direct delete the data instead using a lua expression function. Defaults to True.
        namespace (str, optional): _description_. Defaults to None.
        client (ars.Connection, optional): _description_. Defaults to None.

    Raises:
        Exception: If it's impossible to delete the data

    Returns:
        bool: True if the data was deleted. Otherwise False or exception
    """
    if not client:
        # Get the client
        client = await redis_connect()
    try:
        if not direct:
            if namespace:
                lua = f"for i, name in ipairs(redis.call('KEYS', '{namespace}:*')) do redis.call('DEL', name); end"
            else:
                lua = f"for i, name in ipairs(redis.call('KEYS', '*{key}*')) do redis.call('DEL', name); end"
            if await client.eval(lua, key):
                return True
            else:
                return False
        else:
            await client.delete(key)
            return True
    except ars.ResponseError as message:
        raise Exception(
            f"Impossible to clear the data with key: {key}, because: {message}"
        )


async def save_data(
    client: ars.Connection, key: str, value: str, expire: int = None
) -> any:
    """Save the data to redis database cache.

    You can set also an expiration time in seconds.
    After the expiration time the key will be automatically deleted by redis.

    Args:
        client (ars.Connection): the redis connection async object
        key (str): the unique key of your cache (watch the keybuilder functionality if you want to know how to build a key)
        value (str): the data you want to save in the cache
        expire (int, optional): the expiration time in seconds. Defaults to None and it will be created 3600 second for the object.

    Raises:
        Exception: Response error if it's impossible to save the data

    Returns:
        any: the state of the operation
    """
    try:
        if not expire:
            expire = timedelta(seconds=3600)

        state = await client.set(
            key,
            value=value,
            ex=expire,
        )
        return state
    except ars.ResponseError as message:
        raise Exception(
            f"Impossible to save the data with key: {key}, because: {message}"
        )


async def update_data(
    key: str, new_data: dict, client: ars.Connection = None, expire: int = None
) -> dict:
    """Update a redis cache key with a new data.

    If the key it's not present in the database it will be created a new one.

    Args:
        key (str): the key of your db cache object
        new_data (dict): the new dta you want to save in the cache
        client (ars.Connection, optional): the redis connection client object. Defaults to None.
        expire (int, optional): the expiration time in second. Defaults to None and will be updated to 3600 seconds by default.

    Returns:
        dict: The data inserted in the cache redis db
    """
    if not client:
        # Get the client
        client = await redis_connect()

    # check if the value exist
    data = await get_data(client=client, key=key)

    if data:
        # delete the previous record
        await client.delete(key)

    # create the new object
    new_data = json.dumps(new_data)
    state = await save_data(client=client, key=key, value=new_data, expire=expire)

    if state is True:
        data = json.loads(data)

    return data


async def redis_cache_flow(
    key: str, new_data: dict, expire: int = None, update: bool = False
) -> dict:
    """Function to use the redis cache flow inside your project asynchronously

    Args:
        key (str): the key of your data (please refear to the key builder if you want to generate e useful hash key, but you can use whatever key string you want)
        new_data (dict): the data you want to cache
        update (bool, optional): if you want to force the update of an existing value. Defaults to False.

    Returns:
        dict: the result dict with the key and values inserted
    """
    # Get the client
    client = await redis_connect()

    # First it looks for the data in redis cache
    data = await get_data(client=client, key=key)
    state = False

    # If cache is found then serves the data from cache
    if data is not None:
        if update:
            data = json.dumps(new_data)
            state = await update_data(
                key=key, new_data=new_data, client=client, expire=expire
            )

    # If cache is not found save the object
    else:
        # This block sets saves the respose to redis and serves it directly
        data = json.dumps(new_data)
        state = await save_data(client=client, key=key, value=data, expire=expire)

    if state is True:
        data = json.loads(data)

    await redis_close(client)
    return data


# Global usable functions with asyncio support
def redis_cache(key: str, new_data: dict, **kwargs: dict) -> dict:
    """Function to use the redis cache inside your project synchronously.

    Be careful: if a record it's already in the db with the same key, it will not be updated by default.

    You can set an expiration date with the `expire` (int) parameter.
    You can also set `update` (bool) to True if you want to force the update of a record if it's already present inside the db with the new_data

    Args:
        key (str): your key name to save the data
        new_data (dict): your data to save
        **kwargs (dict): optional arguments to pass to the redis_cache_flow function. For example you can pass expiration time in seconds (int) or update = True if you want to update the data if there is a key already in the cache saved before.

    Returns:
        dict: the data saved inside redis
    """

    result = asyncio.run(redis_cache_flow(key, new_data, **kwargs))
    return result


def redis_cache_delete(key: str, namespace: str = None, direct: bool = True) -> bool:
    """Function to delete a redis cache value inside your project synchronously

    If the record (with the key) is not found inside redis it returns False.

    By default (if direct = True) the function directly delete the value from redis using your key.
    If you want to use a lua script to delete something you can set direct = False and the function will compose a lua script to create a pattern matching with your key and namespace.
    Be carefull because if you use direct = False probably you will delete some other keys and not only a single one

    Args:
        key (str): your key name of the record you want to delete
        namespace (str, optional): if you want to use a namespace to search in the redis db. Defaults to None.
        direct (bool ,otional): If you want to delete directly instead evaluate lua script and do a research. Defaults to False.

    Returns:
        bool: _description_
    """
    result = asyncio.run(clear_data(key, namespace=namespace, direct=direct))
    return result


def redis_cache_keys(pattern: str = "*") -> list:
    """Get the list of keys inside the redis cache db.

    You can use a pattern search query to search inside the database and match different values.

    By default the function research for every values inside the database.

    Args:
        pattern (str, optional): the query search string you want to use. Defaults to "*" to search and gather everything.

    Returns:
        list: the list of the keys founded inside the redis cache db.
    """
    result = asyncio.run(get_list_keys(pattern=pattern))
    return result


def redis_cache_update(key: str, data: dict) -> dict:
    """Redis cache update synchronous function to update a value inside the database.

    If a record is not present, the function will create a new one by default.

    Args:
        key (str): the key of your record
        data (dict): the data you want to update

    Returns:
        dict: the result data after the update or new insert.
    """
    result = asyncio.run(update_data(key, data))
    return result
