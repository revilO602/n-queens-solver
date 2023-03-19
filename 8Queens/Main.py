import random as rn
from ChildIter import ChildIter
from timeit import default_timer as timer
import queue as queue


# Fitness function that counts the amount of attacks on the board
def count_attacks(state):
    attacks = 0
    for x1, y1 in enumerate(state[:-1]):
        for x2 in range(x1 + 1, len(state)):
            y2 = state[x2]
            if (y1 == y2) or (abs(x1 - x2) == abs(y1 - y2)):
                attacks += 1
    return attacks


# Generate random state for board of given size
def random_state(size):
    state = []
    for j in range(0, size):
        state.append(rn.randint(0, size - 1))
    return state


def tabu_search(size):
    MAX_TABU = 20
    tabu_states = queue.Queue()
    parent = random_state(size)
    parent_fitness = count_attacks(parent)
    while parent_fitness != 0:
        found = 0  # did we find a better state in the children
        children = ChildIter(parent, size)
        safe_state = None  # last state that isn't tabu, used to get out of local minimum
        for child in iter(children):
            if child not in tabu_states.queue:
                child_fitness = count_attacks(child)
                if safe_state is None or rn.random() > 0.5:
                    safe_state = child
                if child_fitness < parent_fitness:
                    parent = child
                    parent_fitness = child_fitness
                    found = 1
                    if parent_fitness == 0:
                        break
        if found == 0:
            if len(tabu_states.queue) >= MAX_TABU:
                tabu_states.get()
            tabu_states.put(parent.copy())
            parent = safe_state
            parent_fitness = count_attacks(parent)
    return parent


# Make a list of k states - random or first k states from all
def fill_ray(k, all=None):
    ray = []
    if all is None:
        i = 0
        while i < k:
            state = random_state(size)
            if state not in ray:
                ray.append(state)
                i += 1
    else:
        for i in range(0, k):
            ray.append(list(all[i][0]))
    return ray


def ray_search(size):
    k = 35
    limit = size  # Maximum runtime in seconds - used to determine if the algorithm is stuck
    ray = fill_ray(k)
    start = timer()
    while 1:
        all = {}
        for parent in ray:
            for child in iter(ChildIter(parent, size)):
                child_help = tuple(child.copy())  # Makes child hashable for the dict
                if child_help not in all.keys():
                    child_fitness = count_attacks(child)
                    if child_fitness == 0:  # Found the solution
                        return child
                    all[child_help] = child_fitness
        all = sorted(all.items(), key=lambda item: item[1])
        end = timer()
        if end - start > limit:  # Stuck in local minimum
            return None
        ray = fill_ray(k, all)


# Counts rows from 1 instead of from 0
def print_state(state):
    if state is None:
        print("Got stuck in local minimum")
    for i in state:
        print(str(i + 1), end=' ')
    print('')


def find_solution(size, method):
    if method == ray_search:
        print("RAY SEARCH")
    elif method == tabu_search:
        print("TABU  SEARCH")
    start = timer()
    goal = method(size)
    end = timer()
    print_state(goal)
    print(str(end - start) + '\n')


while 1:
    try:
        size = int(input("Number of queens: "))
    except ValueError:
        print("Please insert valid number")
    else: break
if size < 4:
    print("No solutions exist for less than 4 queens")
else:
    rn.seed()
    find_solution(size, tabu_search)
    find_solution(size, ray_search)


