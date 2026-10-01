"""P1b - Iterative Depth First Search."""

from RMP import dict_gn;

start = 'Arad'
goal = 'Bucharest'
result = ''

def DFS(city, visitedstack):
    global result
    result = result + ' ' + city
    visitedstack.append(city)
    if city == goal:
        return True

    for eachcity in dict_gn[city].keys():
        if eachcity not in visitedstack:
            if DFS(eachcity, visitedstack):
                return True
    visitedstack.pop()
    return False

def main():
    visitedstack = []
    DFS(start, visitedstack)
    print("IDFS Traversal from ", start, " to ", goal, " is: ")
    print(result)

main()
