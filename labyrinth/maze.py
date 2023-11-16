import json
import heapq
import math
import os

#This method prints the path from the start to the end node in the solution file
def build_path(previous, current):
    path = [current]
    #trace back the path from the goal node
    while current in previous:
        current = previous[current]
        path.insert(0, current)

    #write the path to the goal
    with open(solution_file, "w") as f:
        for current in path[1:]:
            f.write(f"{current}\n")
    f.close

#This method calculates the x coordinate value from the hexagonal coordinates
def calculate_x(node):
    return node[0]/2 + node[2]

#This method calculates the y coordinate value from the hexagonal coordinates
def calculate_y(node):
    return math.sqrt(3)*(node[0]/2 + node[1])

#This method calculates the direct distance to the end node using the x-y conversion distance calculation
def h(node):
    return math.sqrt(math.pow(end_x - calculate_x(node), 2) + math.pow(end_y - calculate_y(node), 2))

#This method calculates the neighbours of the given node
def get_neighbours(node):
    a = node[0]
    r = node[1]
    c = node[2]

    #empty list for the neighbours
    ns = []

    #coordinate list of all the possible neighbours the node could have
    poss_neighbours = {(1-a, r-(1-a), c-(1-a)), (1-a, r-(1-a), c+a), (a, r, c-1), (a, r, c+1), (1-a, r+a, c-(1-a)), (1-a, r+a, c+a)}
    
    #if the possible neighbour is not a wall tile and it is in the tiles of the grid, add it as a neighbour
    for n in poss_neighbours:
        if n in possible_tiles:
            ns.append(n)
    neighbours[node] = ns

#This is the a-star algorithm for searching, I used the pseudocode from https://en.wikipedia.org/wiki/A*_search_algorithm to implement it
def a_star():
    node_set = [] #the set of all nodes in the system right now
    heapq.heappush(node_set, (h(start_address), start_address)) #add the start node, using a min heap model for efficiency
    previous = {start_address: None}

    #initialize empty directories
    g_cost = {} #g_cost[n] is the lowest cost from the start to n
    f_cost = {} #f_cost[n] is the lowest possibility cost from start to end if n is in the solution

    #set the intial g and f costs to infinity
    max = float('inf')

    #for each tile, add its address to the g_cost and f_cost key lists and if it is not a wall add it to the possible tiles list
    for tile in tiles:
        address = (tile[0]['a'], tile[0]['r'], tile[0]['c'])
        if tile[1]['type'] != "TileType.WALL":
            possible_tiles.append(address)
        g_cost[address] = max
        f_cost[address] = max

    #for each possible tile, get the neighbours
    for p in possible_tiles:
        get_neighbours(p)
    
    #set the g and f cost of the start node
    g_cost[start_address] = 0
    f_cost[start_address] = h(start_address)

    #while there are available nodes
    while len(node_set) > 0:
        #get the lowest cost next node
        current = heapq.heappop(node_set)
        current_address = current[1]

        #if at the end, build the path
        if current_address == end_address:
            return build_path(previous, current_address)

        #for all the neighbours of the current node
        for n in neighbours[current_address]:
            #add the cost to the neighbour node (always +1 in this case)
            poss_g_cost = g_cost[current_address] + 1
            #if this is less than the current cost to that node
            if poss_g_cost < g_cost[n]:
                previous[n] = current_address #set the current node as the previous node for n
                g_cost[n] = poss_g_cost #update g_cost
                f_cost[n] = poss_g_cost + h(n) #update f_cost

                #if n is currently not being considered in the node set, add it
                if n not in node_set:
                    heapq.heappush(node_set, (h(n), n))
    #should never reach this
    print("FAILED TO FIND A PATH!")

    
if __name__ == "__main__":

    #define my folder paths
    folder_path = "labyrinths"
    folders = ["easy", "extreme", "hard"]

    #open each file
    for folder in folders:
        for filename in os.listdir(os.path.join(folder_path, folder)):
            f = open(os.path.join(folder_path, folder, filename))
            data = json.load(f)
            f.close()

            #create solution directory and name solution file
            maze_name = filename.split("/")[-1].replace(".json", "")
            solutions_folder = "solutions"
            solution_file = f"{os.path.join(solutions_folder, folder, maze_name)}.txt"
            if not os.path.exists(os.path.join(solutions_folder, folder)):
                os.makedirs(os.path.join(solutions_folder, folder))

            #extract data from json
            tiles = data['tiles']
            start = data['start']
            end = data['end']
            start_address = (start['a'], start['r'], start['c'])
            end_address = (end['a'], end['r'], end['c'])

            #create some variables
            possible_tiles = []
            neighbours = {}

            #pre-calculate the x-y coordinate for the end block
            end_x = calculate_x(end_address)
            end_y = calculate_y(end_address)

            #run algorithm
            a_star()
    

