import json
import numpy as np
import heapq
import math


def build_path(previous, current):
    path = [current]
    while current in previous:
        current = previous[current]
        path.insert(0, current)
    print("PATHHHH", path)

def calculate_x(node):
    x = node[0]/2 + node[2]
    return x

def calculate_y(node):
    y = math.sqrt(3)*(node[0]/2 + node[1])
    return y

def h(node):
    return math.sqrt(math.pow(end_x - calculate_x(node), 2) + math.pow(end_y - calculate_y(node), 2))

def get_neighbours(node):
    a = node[0]
    r = node[1]
    c = node[2]
    ns = []
    poss_neighbours = {(1-a, r-(1-a), c-(1-a)), (1-a, r-(1-a), c+a), (a, r, c-1), (a, r, c+1), (1-a, r+a, c-(1-a)), (1-a, r+a, c+a)}
    for n in poss_neighbours:
        if n in possible_tiles:
            ns.append(n)
    neighbours[node] = ns


def a_star():
    node_set = []
    heapq.heappush(node_set, (h(start_address), start_address))
    previous = {start_address: None}

    g_cost = {}
    f_cost = {}

    max = float('inf')
    # print(tiles[0][0])f
    for tile in tiles:
        address = (tile[0]['a'], tile[0]['r'], tile[0]['c'])
        if tile[1]['type'] != "TileType.WALL":
            possible_tiles.append(address)
        g_cost[address] = max
        f_cost[address] = max
    # cost = {json.dumps(tile[0]): max for tile in tiles}
    for p in possible_tiles:
        get_neighbours(p)
    g_cost[start_address] = 0
    f_cost[start_address] = h(start_address)
    # print(cost, sep="\n")

    while len(node_set) > 0:
        current = heapq.heappop(node_set)
        current_address = current[1]
        if current_address == end_address:
            return build_path(previous, current_address)

        for n in neighbours[current_address]:
            poss_g_cost = g_cost[current_address] + 1
            if poss_g_cost < g_cost[n]:
                previous[n] = current_address
                g_cost[n] = poss_g_cost
                f_cost[n] = poss_g_cost + h(n)
                if n not in node_set:
                    heapq.heappush(node_set, (h(n), n))


    print("FAILED!!!")





    
if __name__ == "__main__":

    f = open('labyrinth/labyrinths/easy/labyrinth_00.json')

    data = json.load(f)
    # tiles = data['tiles']
    tiles = data['tiles']
    tilesArr = np.array(tiles)
    start = data['start']
    start_address = (start['a'], start['r'], start['c'])
    # print(start, tiles[0][0])
    possible_tiles = []
    neighbours = {}
    end = data['end']
    end_address = (end['a'], end['r'], end['c'])
    end_x = calculate_x(end_address)
    end_y = calculate_y(end_address)
    a_star()

    f.close()
