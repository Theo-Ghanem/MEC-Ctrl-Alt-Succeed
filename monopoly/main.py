

#28 lines game movement


#4 lines player 
#useful rules:
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
# 1 free parling
# 1 go to jail

# TODO mortgage






starting_budgets = [] # answer: txt file with list of starting budgets (1 integer per line, A,B,C,D)
properties_A = [] # list with properties owned by A
properties_B = [] # list with properties owned by B
properties_C = [] # list with properties owned by C
properties_D = [] # list with properties owned by D

cost_properties_A = 0 # cost of properties owned by A
cost_properties_B = 0 # cost of properties owned by B
cost_properties_C = 0 # cost of properties owned by C
cost_properties_D = 0 # cost of properties owned by D

current_position_A = 0  # current position of A
current_position_B = 0 # current position of B
current_position_C = 0 # current position of C
current_position_D = 0 # current position of D

#set starting budget to 500 (it's the minimum)
starting_budget_A = 500 # starting budget of A
starting_budget_B = 500 # starting budget of B
starting_budget_C = 500 # starting budget of C
starting_budget_D = 500 # starting budget of D
starting_budget_Players = 500

budget_round_5_A = 0 # budget of A at the end of round 5
budget_round_5_B = 0 # budget of B at the end of round 5
budget_round_5_C = 0 # budget of C at the end of round 5
budget_round_5_D = 0 # budget of D at the end of round 5


monopoly_properties = {
   "A1": {"cost": 60, "house_cost": 50, "hotel_rent": 250},
   "A2": {"cost": 60, "house_cost": 50, "hotel_rent": 450},
   "R1": {"cost": 200},
   "B1": {"cost": 60, "house_cost": 50, "hotel_rent": 300},
   "B2": {"cost": 60, "house_cost": 50, "hotel_rent": 300},
   "B3": {"cost": 100, "house_cost": 50, "hotel_rent": 500},
   "C1": {"cost": 100, "house_cost": 50, "hotel_rent": 500},
   "U1": {"cost": 150},
   "C2": {"cost": 100, "house_cost": 50, "hotel_rent": 500},
   "C3": {"cost": 120, "house_cost": 50, "hotel_rent": 600},
   "R2": {"cost": 200},
   "D1": {"cost": 140, "house_cost": 50, "hotel_rent": 700},
   "D2": {"cost": 160, "house_cost": 50, "hotel_rent": 900},
   "D3": {"cost": 160, "house_cost": 50, "hotel_rent": 900},
   "E1": {"cost": 180, "house_cost": 50, "hotel_rent": 1000},
   "E2": {"cost": 200, "house_cost": 50, "hotel_rent": 1100},
   "E3": {"cost": 220, "house_cost": 50, "hotel_rent": 1200},
   "R3": {"cost": 200},
   "F1": {"cost": 220, "house_cost": 50, "hotel_rent": 1200},
   "F2": {"cost": 240, "house_cost": 50, "hotel_rent": 1300},
   "U2": {"cost": 150},
   "F3": {"cost": 260, "house_cost": 50, "hotel_rent": 1400},
   "G1": {"cost": 280, "house_cost": 50, "hotel_rent": 1500},
   "G2": {"cost": 300, "house_cost": 50, "hotel_rent": 1600},
   "G3": {"cost": 320, "house_cost": 50, "hotel_rent": 1700},
   "R4": {"cost": 200},
   "H1": {"cost": 350, "house_cost": 200, "hotel_rent": 2500},
   "H2": {"cost": 400, "house_cost": 200, "hotel_rent": 3000},
}


# Open the file
def readInput(index):
    global properties_A, properties_B, properties_C, properties_D
    global cost_properties_A, cost_properties_B, cost_properties_C, cost_properties_D
    global current_position_A, current_position_B, current_position_C, current_position_D
    global budget_round_5_A, budget_round_5_B, budget_round_5_C, budget_round_5_D

    with open('monopoly\in.txt', 'r') as file:
        lines = file.readlines()[index:index+32]
        for line in lines:
            parts = line.split()
            if len(parts) == 5:  # This box is owned by a player
                property = parts[1].split('_')[0]
                cost = monopoly_properties[property]["cost"]
                if "house_cost" in monopoly_properties[property]:
                    house_cost = monopoly_properties[property]["house_cost"] * int(parts[2])
                box_number = int(parts[0])
                owner = parts[4]
                if owner == 'A':
                    properties_A.append(box_number)
                    cost_properties_A += cost + house_cost
                elif owner == 'B':
                    properties_B.append(box_number)
                    cost_properties_B += cost + house_cost
                elif owner == 'C':
                    properties_C.append(box_number)
                    cost_properties_C += cost + house_cost
                elif owner == 'D':
                    properties_D.append(box_number)
                    cost_properties_D += cost + house_cost
            elif len(parts) == 3:  # This is a player info line
                player = parts[0]
                current_position = int(parts[2])
                if player == 'A':
                    current_position_A = current_position
                    budget_round_5_A = int(parts[1])
                elif player == 'B':
                    current_position_B = current_position
                    budget_round_5_B = int(parts[1])
                elif player == 'C':
                    current_position_C = current_position
                    budget_round_5_C = int(parts[1])
                elif player == 'D':
                    current_position_D = current_position
                    budget_round_5_D = int(parts[1])

def update_budgets(A, B, C, D):
    global starting_budget_A, starting_budget_B, starting_budget_C, starting_budget_D
    starting_budget_A += A
    starting_budget_B += B
    starting_budget_C += C
    starting_budget_D += D



# find the number of times each player has gone around the board to see if they got +200$
def calculate_rounds_and_add_bonus(properties, current_position):
    properties.sort()
    rounds = 0
    for i in range(1, len(properties)):
        if properties[i] < properties[i - 1]: # if the next property is smaller than the previous one, it means we went around the board
            rounds += 1
    if current_position < max(properties): # if the current position is smaller than the biggest property, it means we went around the board
        rounds += 1
    if current_position < min(properties): # if the current position is smaller than the smallest property, it means we went around the board
        rounds += 1
    update_budgets(rounds * 200, rounds * 200, rounds * 200, rounds * 200)    
    return rounds

def print_properties_owned_by_each_player():
    print("Properties owned by A:", properties_A)
    print("Properties owned by B:", properties_B)
    print("Properties owned by C:", properties_C)
    print("Properties owned by D:", properties_D)
def print_current_position_of_each_player():
    print("Current position of A:", current_position_A)
    print("Current position of B:", current_position_B)
    print("Current position of C:", current_position_C)
    print("Current position of D:", current_position_D)
def print_rounds_of_each_player():
    rounds_A = calculate_rounds_and_add_bonus(properties_A, current_position_A)
    rounds_B = calculate_rounds_and_add_bonus(properties_B, current_position_B)
    rounds_C = calculate_rounds_and_add_bonus(properties_C, current_position_C)
    rounds_D = calculate_rounds_and_add_bonus(properties_D, current_position_D)
    print("Player A has gone around the board", rounds_A, "times")
    print("Player B has gone around the board", rounds_B, "times")
    print("Player C has gone around the board", rounds_C, "times")
    print("Player D has gone around the board", rounds_D, "times")
def print_cost_of_properties_owned_by_each_player():
    print("Spent on properties by A:", cost_properties_A)
    print("Spent on properties by B:", cost_properties_B)
    print("Spent on properties by C:", cost_properties_C)
    print("Spent on properties by D:", cost_properties_D)
def print_budgets_after_round_5():
    print("Budget of A after round 5:", budget_round_5_A)
    print("Budget of B after round 5:", budget_round_5_B)
    print("Budget of C after round 5:", budget_round_5_C)
    print("Budget of D after round 5:", budget_round_5_D)
def main():
    readInput(0)
    # print_properties_owned_by_each_player()
    # print_current_position_of_each_player()
    # print_rounds_of_each_player()
    print_budgets_after_round_5()
    print_cost_of_properties_owned_by_each_player()
    # with open('monopoly\out.txt', 'w') as f:
    #    f.write(str(starting_budget_Players) + '\n')

if __name__ == "__main__":
    main()




