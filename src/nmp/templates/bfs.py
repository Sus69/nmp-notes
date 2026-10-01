"""P1a - Breadth First Search."""

import queue as Q
from RMP import dict_gn;

start = 'Arad'
goal = 'Bucharest'
result = ''

def BFS(city, cityq, visited):
    global result
    visited.add(city)
    result = result + ' ' + city
    if city == goal:
        return True
    for eachcity in dict_gn[city].keys():
        if eachcity not in visited and eachcity not in cityq.queue:
            cityq.put(eachcity)
    if cityq.empty():
        return False
    return BFS(cityq.get(), cityq, visited)

def main():
    cityq = Q.Queue()
    visited = set()
    BFS(start, cityq, visited)
    print("BFS Traversal from", start, "to", goal, "is: ")
    print(result)

main()
