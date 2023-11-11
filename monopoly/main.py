# Note: we did not end up using all of them because we do not have enough information
# about the players and where they landed
# useful rules: 
# if you land on a property, you can buy it if you have enough money
# if you land on a property owned by someone else, you pay rent
# if you land on a property owned by yourself, you do nothing
# if you land on a property owned by the bank, you can buy it if you have enough money
# every time you pass Go you get 200 from the bank

# there are 40 boxes on the board
# 28 properties
# 3 chance
# 3 community chest
# 1 luxury tax
# 1 income tax
# 1 jail
# 1 free parking
# 1 go to jail


import os

# dictionary with all the monopoly properties and their costs
# https://www.monopolyland.com/monopoly-properties-list-with-prices/
monopoly_properties = {
   "A1": {"cost": 60, "house_cost": 50},
   "A2": {"cost": 60, "house_cost": 50},
   "R1": {"cost": 200},
   "B1": {"cost": 60, "house_cost": 50},
   "B2": {"cost": 60, "house_cost": 50},
   "B3": {"cost": 100, "house_cost": 50},
   "C1": {"cost": 100, "house_cost": 50},
   "U1": {"cost": 150},
   "C2": {"cost": 100, "house_cost": 50},
   "C3": {"cost": 120, "house_cost": 50},
   "R2": {"cost": 200},
   "D1": {"cost": 140, "house_cost": 50},
   "D2": {"cost": 160, "house_cost": 50},
   "D3": {"cost": 160, "house_cost": 50},
   "E1": {"cost": 180, "house_cost": 50},
   "E2": {"cost": 200, "house_cost": 50},
   "E3": {"cost": 220, "house_cost": 50},
   "R3": {"cost": 200},
   "F1": {"cost": 220, "house_cost": 50},
   "F2": {"cost": 240, "house_cost": 50},
   "U2": {"cost": 150},
   "F3": {"cost": 260, "house_cost": 50},
   "G1": {"cost": 280, "house_cost": 50},
   "G2": {"cost": 300, "house_cost": 50},
   "G3": {"cost": 320, "house_cost": 50},
   "R4": {"cost": 200},
   "H1": {"cost": 350, "house_cost": 200},
   "H2": {"cost": 400, "house_cost": 200}
}


# players dictionary
players = {
    'A': {'properties': [], 'cost': 0, 'end_position': 0, 'end_budget': 0},
    'B': {'properties': [], 'cost': 0, 'end_position': 0, 'end_budget': 0},
    'C': {'properties': [], 'cost': 0, 'end_position': 0, 'end_budget': 0},
    'D': {'properties': [], 'cost': 0, 'end_position': 0, 'end_budget': 0},
}


# read the input file and populate the players dictionary
def readInput(index):
    with open('monopoly\in.txt', 'r') as file:
        lines = file.readlines()[index:index+32]
        for line in lines:
            parts = line.split()
            if len(parts) == 5:  # This box is owned by a player
                property = parts[1].split('_')[0]
                cost = monopoly_properties[property]["cost"]
                house_cost = monopoly_properties[property].get("house_cost", 0) * int(parts[2])
                box_number = int(parts[0])
                owner = parts[4]
                players[owner]['properties'].append(box_number)
                players[owner]['cost'] += cost + house_cost
            elif len(parts) == 3:  # This is a player info line
                player = parts[0]
                players[player]['end_position'] = int(parts[2])
                players[player]['end_budget'] = int(parts[1])


# find the number of times each player has gone around the board to see if they got +200$ from the bank
def calculate_rounds(player):
    properties = players[player]['properties']
    if not properties:  # if the player has no properties return 0 ( we assume they havent gone around the board)
        return 0
    properties.sort()
    current_position = players[player]['end_position']
    rounds = 0
    for i in range(1, len(properties)):
        if properties[i] < properties[i - 1]: # if the next property is smaller than the previous one, it means we went around the board
            rounds += 1
    if current_position < max(properties): # if the current position is smaller than the biggest property, it means we went around the board
        rounds += 1
    if current_position < min(properties): # if the current position is smaller than the smallest property, it means we went around the board
        rounds += 1    
    return rounds


# calculate the starting budget of each player
def calculate_starting_budgets():
    min_starting_budget = 0
    for player in players.keys():
        rounds = calculate_rounds(player)
        players[player]['starting_budget'] = players[player]['end_budget'] + players[player]['cost'] - rounds * 200

    min_starting_budget = min(players[player]['starting_budget'] for player in players.keys())

    if min_starting_budget < 500: # if the minimum starting budget is less than 500, we set it to 500
        min_starting_budget = 500
    elif min_starting_budget > 2500: # if the minimum starting budget is more than 2500, we set it to 2500
        min_starting_budget = 2500
    return min_starting_budget


# Useful for checking the results
def print_properties_owned_by_each_player():
    for player in players.keys():
        print(f"Properties owned by {player}:", players[player]['properties'])

def print_current_position_of_each_player():
    for player in players.keys():
        print(f"Current position of {player}:", players[player]['end_position'])

def print_rounds_of_each_player():
    for player in players.keys():
        rounds = calculate_rounds(player)
        print(f"Player {player} has gone around the board", rounds, "times")

def print_cost_of_properties_owned_by_each_player():
    for player in players.keys():
        print(f"Spent on properties by {player}:", players[player]['cost'])

def print_budgets_after_round_5():
    for player in players.keys():
        print(f"Budget of {player} after round 5:", players[player]['end_budget'])
    

def main():
    if os.path.exists('monopoly\out.txt'):
        os.remove('monopoly\out.txt')

    with open('monopoly\out.txt', 'a') as output:
        for i in range(0, 32000, 32):
            global players
            players = {
                'A': {'properties': [], 'cost': 0, 'end_position': 0, 'end_budget': 0},
                'B': {'properties': [], 'cost': 0, 'end_position': 0, 'end_budget': 0},
                'C': {'properties': [], 'cost': 0, 'end_position': 0, 'end_budget': 0},
                'D': {'properties': [], 'cost': 0, 'end_position': 0, 'end_budget': 0},
            }
            readInput(i)
            output.write(str(calculate_starting_budgets()) + '\n')
        

if __name__ == "__main__":
    main()