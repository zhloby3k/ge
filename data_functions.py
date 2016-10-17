def wrapper(fn, data):
    cache = {}
    def wrapped(*args, i = 0):
        try:
            calculated = cache[args]
            return calculated[i]
        except KeyError:
            cache[args] = calculated = fn(data, *args)
            return calculated[i]
    return wrapped
