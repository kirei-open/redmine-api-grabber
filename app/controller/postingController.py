from app.services import posting, redisCache

async def get_all_post(cache, x_token):
    print('controller')
    key = f"posting"
    in_cache = await redisCache.get_redis_cache( cache, x_token, key)
    if in_cache is not None:
        return in_cache
    data = posting.get_post();
    await redisCache.set_redis_cache(data, cache, x_token, key)
    return data

async def get_laporan(cache, x_token):
    key = f"laporan"
    in_cache = await redisCache.get_redis_cache( cache, x_token, key)
    if in_cache is not None:
        return in_cache
    data = posting.get_laporan(token=x_token);
    await redisCache.set_redis_cache(data, cache, x_token, key)
    return data

def create_new_absent(deskripsi, photo, x_token):
    data = posting.create_absent(deskripsi=deskripsi, photo=photo, x_token = x_token)
    return data
