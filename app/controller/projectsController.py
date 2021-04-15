from app.services import redmine , redisCache



async def get_all_projects(cache, x_token):
    key = f"redminegetallproject"
    in_cache = await redisCache.get_redis_cache( cache, x_token, key)
    if in_cache is not None:
        return in_cache
    data = redmine.get_all_projects()
    await redisCache.set_redis_cache(data, cache, x_token, key)
    return data

async def get_all_project_summary(cache, x_token):
    key = f"redminegetsummary"
    in_cache = await redisCache.get_redis_cache( cache, x_token, key)
    if in_cache is not None:
        return in_cache
    data = redmine.get_all_project_summary()
    await redisCache.set_redis_cache(data, cache, x_token, key)
    return data

async def get_all_project_detail(cache, x_token):
    key = f"getprojectdetail"
    in_cache = await redisCache.get_redis_cache( cache, x_token, key)
    if in_cache is not None:
        return in_cache
    data =  redmine.get_all_project_detail()
    await redisCache.set_redis_cache(data, cache, x_token, key)
    return data

async def get_project_by_id(id, cache, x_token):
    key = f"getprojectid_{id}"
    in_cache = await redisCache.get_redis_cache( cache, x_token, key)
    if in_cache is not None:
        return in_cache
    data =  redmine.get_project_by_id(id)
    await redisCache.set_redis_cache(data, cache, x_token, key)
    return data