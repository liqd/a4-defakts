import random
import time
from collections import defaultdict

counts = defaultdict(int)


def timeit(func):
    def wrapped_func(*args, **kwargs):
        counts["calls"] += 1

        start = time.time()

        result = func(*args, **kwargs)

        end = time.time()

        if random.randint(1, 1000) == 1000:
            counts["id"] += 1

            for key, value in counts.items():
                print(f"{key}: {round(value, 3)}")

        counts[func.__name__] += end - start
        counts[f"{func.__name__}_calls"] += 1

        return result

    return wrapped_func
