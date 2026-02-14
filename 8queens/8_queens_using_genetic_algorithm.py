#imports
import random

#Problem Parameters
NUM_QUEENS = 8
POPULATION_SIZE = 100 
MUTATION_RATE = 0.1 
MAX_FITNESS = 28  #NUM_QUEENS *(NUM_QUEENS-1)/2

#Creates a random board
def create_board():
    return [random.randint(0, NUM_QUEENS - 1) for _ in range(NUM_QUEENS)]


#The number of non-attacking pairs of queens on a board
def fitness(board):
    clashes = 0 
    for i in range(NUM_QUEENS):
        for j in range(i + 1, NUM_QUEENS):
            if board[i] == board[j] or abs(board[i] - board[j]) == abs(i - j):
                clashes += 1
    return MAX_FITNESS - clashes #28 - clashes


#Roulette wheel selection
def selection(population):
    selected_population = [] 

    fitness_values = [fitness(board) for board in population]
    total_fitness = sum(fitness_values)

    normalized_fitness = [each / total_fitness for each in fitness_values]

    for _ in range(POPULATION_SIZE):
        value = random.random()
        probability_sum = 0
        for i in range(POPULATION_SIZE):
            probability_sum += normalized_fitness[i]
            if probability_sum >= value:
                selected_population.append(population[i])
                break

    return selected_population


#Crossover between two parents(boards) to create two children.
def Crossover(parent1, parent2):
    crossover_point = random.randint(1, NUM_QUEENS - 1) #Random Point
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]

    return child1, child2


#Mutates a board with a certain probability.
def mutation(board):
    if random.random() < MUTATION_RATE:
        idx = random.randint(0, NUM_QUEENS - 1)
        new_value = random.randint(0, NUM_QUEENS - 1)
        while new_value == board[idx]:
            new_value = random.randint(0, NUM_QUEENS - 1)
        board[idx] = new_value

    return board
    

#Prints the board with queens represented by 'Q'.
def print_chess_board(board):
    for row in range(NUM_QUEENS + 1):
        print(row - 1 if row != 0 else ' ', end=' ')#print x axis
    print()
    for row in range(NUM_QUEENS - 1, -1, -1):
        print(row, end=' ')#print y axis
        for col in range(NUM_QUEENS):
            print('Q' if board[col] == row else '-', end=' ')
        print()


#Prints the solution found by the genetic algorithm.
def print_solution(best_fitness, best_board, generation):
    print("\n" + "="*51)
    if best_fitness != MAX_FITNESS:
        print("No optimal solution found.")
    else:
        print(f"Optimal solution found in {generation + 1} generations:")
        print(f"Board: {best_board}")
        print(f"Fitness: {best_fitness}")
        print("="*51)
        print_chess_board(best_board)


#The genetic algorithm to solve the N-Queens problem."""
def genetic_algorithm(num_generations):
    population = [create_board() for _ in range(POPULATION_SIZE)] 
    best_fitness = 0
    best_board = None

    for generation in range(num_generations):
        #selection
        selected_population = selection(population)

        #crossover
        children = []
        for i in range(0, POPULATION_SIZE, 2):
            parent1 = selected_population[i]
            parent2 = selected_population[i+1]
            child1, child2 = Crossover(parent1, parent2)
            children.append(child1)
            children.append(child2)
            
        #Mutation
        for child in children:
            mutation(child)

        # new population
        population = children 

        #update best solution
        current_fitness = max(fitness(board) for board in population)

        if current_fitness > best_fitness:
            best_fitness = current_fitness
            best_board = max(population, key = fitness)

        #print progress
        print(f'\rGeneration: {generation + 1}, best fitness: {best_fitness}', end = '')

        if current_fitness == MAX_FITNESS: #28
            break

    #print solution
    print_solution(best_fitness, best_board, generation)


if __name__ == "__main__":
    print("="*51)
    num_generations = int(input("Enter the number of generations: "))
    print("="*51)
    genetic_algorithm(num_generations)