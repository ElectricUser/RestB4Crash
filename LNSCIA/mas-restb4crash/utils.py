import random
from queue import Queue

# Stress > 5, 3 times in a row == stressed out
FIFO_queue = Queue(maxsize=5)
FIFO_queue.put(1)
FIFO_queue.put(2)
FIFO_queue.put(3)
FIFO_queue.put(4)
FIFO_queue.put(5)


def random_number_generator():
    number = random.randint(0, 10)
    return number


def update_stress(stress_levels: Queue, val):
    if stress_levels.full():
        stress_levels.get()  # remove
        stress_levels.put(val)  # put
    else:
        stress_levels.put(val)

    return True


"""def is_stressed(stress_levels: Queue):
    stressed = None
    stress_list = list(stress_levels.queue)
    for val in stress_list:
"""
