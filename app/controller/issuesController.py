from app.services import redmine, redisCache


async def get_recent_issues(cache, x_token):
    key = f"getissuesrecent"
    in_cache = await redisCache.get_redis_cache( cache, x_token, key)
    if in_cache is not None:
        return in_cache
    data = redmine.get_most_recent_issues()[0]
    await redisCache.set_redis_cache(data, cache, x_token, key)
    return data

async def graph_issues(sdate, edate , cache, x_token):
    key = f"getissuesgraph_{sdate}_{edate}"
    in_cache = await redisCache.get_redis_cache_graph( cache, x_token, key)
    if in_cache is not None:
        return in_cache
    data = redmine.get_issues_graph(sdate, edate)
    await redisCache.set_redis_cache_graph(data, cache, x_token, key)
    return data

async def get_assigned_issues(name, cache, x_token):
    key = f"getassignedissues_{name}"
    in_cache = await redisCache.get_redis_cache( cache, x_token, key)
    if in_cache is not None:
        return in_cache
    data = redmine.get_issues_assigned_for(name)
    await redisCache.set_redis_cache(data, cache, x_token, key)
    return data