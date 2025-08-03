import random
import numpy as np

# Inicializa população com rotas para os veículos
def initialize_population(num_clients, population_size, num_vehicles, clients, vehicle_capacity):
    if num_clients == 0 or num_vehicles < 1:
        raise ValueError("Número de clientes deve ser maior que 0 e número de veículos pelo menos 1")
    
    population = []
    for _ in range(population_size):
        individual = [[] for _ in range(num_vehicles)]
        client_indices = list(range(num_clients))
        random.shuffle(client_indices)
        current_vehicle = 0
        current_capacity = 0
        for idx in client_indices:
            demand = clients[idx][1]
            if current_vehicle < num_vehicles:
                if current_capacity + demand <= vehicle_capacity:
                    individual[current_vehicle].append(idx)
                    current_capacity += demand
                else:
                    current_vehicle += 1
                    if current_vehicle < num_vehicles:
                        individual[current_vehicle].append(idx)
                        current_capacity = demand
                    else:
                        for i in range(num_vehicles):
                            if sum(clients[j][1] for j in individual[i]) + demand <= vehicle_capacity:
                                individual[i].append(idx)
                                break
        population.append(individual)
    return population

# Calcula aptidão (distância total) usando matriz de distâncias
def calculate_fitness(individual, clients, depot, vehicle_capacity, distance_matrix):
    total_distance = 0
    attended_clients = set()
    for route in individual:
        route_demand = sum(clients[idx][1] for idx in route if idx < len(clients))
        if route_demand > vehicle_capacity:
            return float('inf')
        prev_idx = 0  # Depósito (índice 0 na matriz)
        for idx in route:
            if idx < len(clients):
                total_distance += distance_matrix[prev_idx][idx + 1]  # +1 porque depósito é índice 0
                prev_idx = idx + 1
                attended_clients.add(idx)
        total_distance += distance_matrix[prev_idx][0]  # Volta ao depósito
    if len(attended_clients) != len(clients):
        return float('inf')
    return total_distance

# Seleciona pais com base na aptidão
def select_parents(population, fitness_values, num_parents):
    sorted_indices = np.argsort(fitness_values)
    return [population[i] for i in sorted_indices[:num_parents]]

# Realiza cruzamento entre pais
def crossover(parent1, parent2, clients, vehicle_capacity):
    num_vehicles = max(len(parent1), len(parent2))
    child1 = [[] for _ in range(num_vehicles)]
    child2 = [[] for _ in range(num_vehicles)]
    
    for i in range(num_vehicles):
        if i < len(parent1) and (i >= len(parent2) or random.random() < 0.5):
            route = parent1[i][:]
        else:
            route = parent2[i][:] if i < len(parent2) else []
        route_demand = sum(clients[idx][1] for idx in route if idx < len(clients))
        while route_demand > vehicle_capacity and route:
            route.pop()
            route_demand = sum(clients[idx][1] for idx in route if idx < len(clients))
        child1[i] = route
        
        if i < len(parent2) and (i >= len(parent1) or random.random() < 0.5):
            route = parent2[i][:]
        else:
            route = parent1[i][:] if i < len(parent1) else []
        route_demand = sum(clients[idx][1] for idx in route if idx < len(clients))
        while route_demand > vehicle_capacity and route:
            route.pop()
            route_demand = sum(clients[idx][1] for idx in route if idx < len(clients))
        child2[i] = route
    
    child1 = ensure_all_clients(child1, clients, vehicle_capacity)
    child2 = ensure_all_clients(child2, clients, vehicle_capacity)
    return child1, child2

# Garante que todos os clientes sejam atendidos
def ensure_all_clients(individual, clients, vehicle_capacity):
    num_vehicles = len(individual)
    all_clients = set(range(len(clients)))
    attended = set(idx for route in individual for idx in route)
    missing = list(all_clients - attended)
    
    for idx in missing:
        demand = clients[idx][1]
        added = False
        for route in individual:
            route_demand = sum(clients[i][1] for i in route if i < len(clients))
            if route_demand + demand <= vehicle_capacity:
                route.append(idx)
                added = True
                break
        if not added:
            for i in range(num_vehicles):
                if sum(clients[j][1] for j in individual[i]) + demand <= vehicle_capacity:
                    individual[i].append(idx)
                    added = True
                    break
            if not added:
                individual.append([idx])
    
    while len(individual) < num_vehicles:
        individual.append([])
    if len(individual) > num_vehicles:
        individual = individual[:num_vehicles]
    return individual

# Aplica mutações nas rotas
def mutate(individual, mutation_rate, clients, vehicle_capacity):
    for route in individual:
        if random.random() < mutation_rate and len(route) >= 2:
            i, j = random.sample(range(len(route)), 2)
            route[i], route[j] = route[j], route[i]
        if random.random() < mutation_rate and route and len(individual) > 1:
            client_idx = random.choice(route)
            route.remove(client_idx)
            new_route_idx = random.choice([i for i in range(len(individual)) if individual[i] != route])
            new_route_demand = sum(clients[idx][1] for idx in individual[new_route_idx] if idx < len(clients))
            if new_route_demand + clients[client_idx][1] <= vehicle_capacity:
                individual[new_route_idx].append(client_idx)
    return ensure_all_clients(individual, clients, vehicle_capacity)