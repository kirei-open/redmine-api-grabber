from fastapi import Depends, Header
from app.middleware import Jwtdecode
from datetime import datetime
from dotenv import load_dotenv
import datetime
import json
import os 

load_dotenv()

exp = int(os.getenv('EXPIRE_CACHE'))
prefix = os.getenv('PREFIX_CACHE')

async def get_redis_cache(cache, x_token, key):
    user = Jwtdecode.decoded(token=x_token)
    redis_key = prefix + '_' + key + '_{}'.format(user['id'])
    redis_key = redis_key.replace(" ", "")
    get_cache = await cache.get(redis_key)
    if get_cache is not None:
        # print('GET REDIS CACHE')
        return json.loads(get_cache)
    return None

async def set_redis_cache(data,cache,x_token,key):
    user = Jwtdecode.decoded(token=x_token)
    redis_key = prefix + '_' + key + '_{}'.format(user['id'])
    redis_key = redis_key.replace(" ", "")
    # print('SET DATA TO REDIS')
    await cache.set(redis_key,json.dumps(data),expire=exp)
    return data

def myconverter(o):
        if isinstance(o, datetime.datetime):
            return o.__str__()

async def set_redis_cache_graph(data, cache, x_token, key):
    user = Jwtdecode.decoded(token=x_token)
    redis_key = prefix + '_' + key + '_{}'.format(user['id'])
    redis_key = redis_key.replace(" ", "")
    get_cache = await cache.get(redis_key)
    # print('GET DATABASE SET TO REDIS')
    await cache.set(redis_key,json.dumps(data, default=myconverter),expire=exp)
    return data

async def get_redis_cache_graph(cache, x_token, key):
    user = Jwtdecode.decoded(token=x_token)
    redis_key = prefix + '_' + key + '_{}'.format(user['id'])
    redis_key = redis_key.replace(" ", "")
    get_cache = await cache.get(redis_key)
    if get_cache is not None:
        # print('GET REDIS CACHE')
        data = []
        in_cache = json.loads(get_cache)
        for i in in_cache:
            i['date'] = i['date'].replace(" ","T")
            data.append(i)
        return data
    return None

async def redis_cache_delete(cache, x_token, key):
    user = Jwtdecode.decoded(token=x_token)
    redis_key = prefix + '_' + key + '_{}'.format(user['id'])
    redis_key = redis_key.replace(" ", "")
    get_cache = await cache.get(redis_key)
    if get_cache is not None:
        await cache.delete(redis_key)
        # print('delete redis cache')
