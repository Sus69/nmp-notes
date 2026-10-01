"""P2a - A* Search."""

import queue as Q
from RMP import dict_gn;
from RMP import dict_hn;

start = 'Arad'
goal = 'Bucharest'
result = ''

def get_fn(citystr):
    cities = citystr.split(",")
    gn = 0

    for ctr in range(0, len(cities) - 1):
        gn = gn + dict_gn[cities[ctr]][cities[ctr+1]]

    hn = dict_hn[cities[-1]]
    return(gn + hn)

def main():
    global result
    cityq = Q.PriorityQueue()
    closed = set()

    cityq.put((get_fn(start), start, start))

    while not cityq.empty():
        f_score, current_path_str, current_city = cityq.get()

        if current_city in closed:
            continue
        closed.add(current_city)

        if current_city == goal:
            result = current_path_str + "::" + str(f_score)
            break

        for neighbor_city in dict_gn[current_city]:
            if neighbor_city in closed:
                continue
            new_path_str = current_path_str + "," + neighbor_city
            new_f_score = get_fn(new_path_str)
            cityq.put((new_f_score, new_path_str, neighbor_city))

    print("The A* path with the total is: ")
    print(result)

main()
