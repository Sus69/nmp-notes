"""P2b - Recursive Best-First Search."""

import queue as Q
from RMP import dict_gn;
from RMP import dict_hn;

start = 'Arad'
goal = 'Bucharest'
result = ''
MAX_DEPTH = 50

def get_fn(citystr):
    cities = citystr.split(",")
    hn = gn = 0

    for ctr in range(0, len(cities) - 1):
        gn = gn + dict_gn[cities[ctr]][cities[ctr+1]]

    hn = dict_hn[cities[len(cities)-1]]
    return(hn + gn)

def printout(cityq):
    for i in range(0, cityq.qsize()):
        print(cityq.queue[i])

def expand(cityq, depth=0):
    global result
    if cityq.empty() or depth > MAX_DEPTH:
        return
    tot, citystr, thiscity = cityq.get()
    nexttot = 999

    if not cityq.empty():
        nexttot, nextcitystr, nextthiscity = cityq.queue[0]

    if thiscity == goal and tot < nexttot:
        result = citystr + "::" + str(tot)
        return

    print("\nExpanded city -------", thiscity)
    print("Second bestf(n) -------", nexttot)
    tempq = Q.PriorityQueue()

    for cty in dict_gn[thiscity]:
        if cty not in citystr.split(","):
            tempq.put((get_fn(citystr + "," + cty), citystr + "," + cty, cty))

    if tempq.empty():
        expand(cityq, depth + 1)
        return

    for ctr in range(min(2, tempq.qsize())):
        ctrtot, ctrcitystr, ctrthiscity = tempq.get()
        if ctrtot < nexttot:
            cityq.put((ctrtot, ctrcitystr, ctrthiscity))
        else:
            cityq.put((ctrtot, citystr, thiscity))
            break

    printout(cityq)
    expand(cityq, depth + 1)

def main():
    cityq = Q.PriorityQueue()
    thiscity = start
    cityq.put((999, "NA", "NA"))
    cityq.put((get_fn(start), start, thiscity))
    expand(cityq)
    print(result)

main()
