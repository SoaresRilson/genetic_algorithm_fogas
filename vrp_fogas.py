import pygame
import random
import numpy as np
from genetic_algorithm import initialize_population, calculate_fitness, select_parents, crossover, mutate

# Inicializa o Pygame
pygame.init()

# Configura a janela
width, height = 1000, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Fogás VRP - Algoritmo Genético")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Gera cores dinâmicas para os veículos
def generate_vehicle_colors(num_vehicles):
    colors = []
    for i in range(num_vehicles):
        hue = (i * 360 // num_vehicles) % 360
        r = int(255 * (1 if hue < 120 or hue > 240 else (240 - hue) / 120 if 120 <= hue <= 240 else 0))
        g = int(255 * (1 if 0 < hue < 120 else (hue - 120) / 120 if 120 <= hue <= 240 else 0))
        b = int(255 * (1 if hue > 120 else (360 - hue) / 120 if 240 <= hue <= 360 else 0))
        colors.append((r, g, b))
    return colors

# Define depósito e 30 clientes
depot = (400, 100)
clients = [
    ((450, 120), 10), ((520, 180), 15), ((580, 140), 5), ((650, 200), 20), ((720, 160), 10),
    ((780, 220), 15), ((600, 250), 5), ((500, 300), 10), ((700, 280), 15), ((550, 350), 20),
    ((800, 150), 10), ((750, 200), 5), ((620, 320), 15), ((480, 400), 10), ((680, 360), 5),
    ((900, 100), 20), ((850, 180), 15), ((500, 450), 10), ((600, 400), 5), ((700, 450), 15),
    ((420, 200), 10), ((550, 100), 5), ((650, 150), 15), ((750, 300), 20), ((800, 400), 10),
    ((900, 250), 15), ((450, 500), 5), ((580, 480), 10), ((700, 500), 15), ((620, 200), 20)
]

# Parâmetros do problema
num_vehicles = 5
vehicle_capacity = 100

# Verifica viabilidade da demanda
total_demand = sum(client[1] for client in clients)
if total_demand > num_vehicles * vehicle_capacity:
    raise ValueError("A Demanda total excede a capacidade da frota")

if len(clients) == 0:
    raise ValueError("A lista de clientes não pode estar vazia")
if num_vehicles < 1:
    raise ValueError("O número de veículos deve ser pelo menos 1")

# Parâmetros do algoritmo genético
population_size = max(50, len(clients) * 2)
num_generations = 2000
mutation_rate = 0.05

# Cria matriz de distâncias
def create_distance_matrix(depot, clients):
    n = len(clients) + 1
    matrix = np.zeros((n, n))
    points = [(depot[0], depot[1])] + [client[0] for client in clients]
    for i in range(n):
        for j in range(n):
            if i != j:
                matrix[i][j] = np.sqrt((points[i][0] - points[j][0]) ** 2 + (points[i][1] - points[j][1]) ** 2)
    return matrix

# Desenha as rotas
def draw_routes(screen, routes, clients, depot, vehicle_colors):
    for i, route in enumerate(routes):
        color = vehicle_colors[i % len(vehicle_colors)]
        prev_point = depot
        for client_idx in route:
            if client_idx < len(clients):
                client_point = clients[client_idx][0]
                pygame.draw.line(screen, color, prev_point, client_point, 2)
                prev_point = client_point
        pygame.draw.line(screen, color, prev_point, depot, 2)
    pygame.draw.circle(screen, RED, depot, 10)
    for client, _ in clients:
        pygame.draw.circle(screen, BLUE, client, 5)

# Desenha gráfico da evolução da aptidão
def draw_plot(screen, fitness_history, num_generations):
    plot_x, plot_y = 50, 50
    plot_width, plot_height = 300, 300
    font = pygame.font.SysFont('arial', 12)
    
    # Desenha fundo e bordas
    pygame.draw.rect(screen, WHITE, (plot_x, plot_y, plot_width, plot_height))
    pygame.draw.rect(screen, BLACK, (plot_x, plot_y, plot_width, plot_height), 2)
    
    if not fitness_history:
        return
    
    # Escala os valores de aptidão
    max_fitness = max(fitness_history) * 1.1
    min_fitness = min(fitness_history) * 0.9 if fitness_history else 0
    if max_fitness == min_fitness:
        max_fitness = min_fitness + 1
    
    # Desenha linha do gráfico
    points = []
    for i, fitness in enumerate(fitness_history):
        x = plot_x + (i / max(1, len(fitness_history) - 1)) * plot_width
        y = plot_y + plot_height - ((fitness - min_fitness) / (max_fitness - min_fitness)) * plot_height
        points.append((x, y))
    
    for i in range(len(points) - 1):
        pygame.draw.line(screen, GREEN, points[i], points[i + 1], 2)
    
    # Desenha eixos com rótulos
    pygame.draw.line(screen, BLACK, (plot_x, plot_y + plot_height), (plot_x + plot_width, plot_y + plot_height), 2)
    pygame.draw.line(screen, BLACK, (plot_x, plot_y), (plot_x, plot_y + plot_height), 2)
    
    # Rótulos do eixo x (gerações)
    for i in range(0, num_generations + 1, num_generations // 5):
        x = plot_x + (i / num_generations) * plot_width
        label = font.render(str(i), True, BLACK)
        screen.blit(label, (x - 10, plot_y + plot_height + 5))
    
    # Rótulos do eixo y (aptidão)
    for i in range(5):
        fitness = min_fitness + (max_fitness - min_fitness) * (i / 4)
        y = plot_y + plot_height - (i / 4) * plot_height
        label = font.render(f"{int(fitness)}", True, BLACK)
        screen.blit(label, (plot_x - 40, y - 6))

# Função principal
def main():
    vehicle_colors = generate_vehicle_colors(num_vehicles)
    distance_matrix = create_distance_matrix(depot, clients)
    population = initialize_population(len(clients), population_size, num_vehicles, clients, vehicle_capacity)
    
    # Inicializa melhor solução e histórico de aptidão
    fitness_values = [calculate_fitness(individual, clients, depot, vehicle_capacity, distance_matrix) for individual in population]
    valid_solutions = [i for i, f in enumerate(fitness_values) if f != float('inf')]
    if not valid_solutions:
        raise ValueError("Nenhuma solução inicial válida encontrada.")
    best_solution = population[valid_solutions[0]]
    best_fitness = fitness_values[valid_solutions[0]]
    fitness_history = [best_fitness]
    
    running = True
    generation = 0
    while running and generation < num_generations:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                running = False
        
        # Avalia aptidão e atualiza melhor solução
        fitness_values = [calculate_fitness(individual, clients, depot, vehicle_capacity, distance_matrix) for individual in population]
        min_fitness = min(fitness_values)
        if min_fitness < best_fitness:
            best_fitness = min_fitness
            best_solution = population[fitness_values.index(min_fitness)]
        fitness_history.append(min_fitness)
        
        # Desenha gráfico e rotas
        screen.fill(WHITE)
        draw_plot(screen, fitness_history, num_generations)
        draw_routes(screen, best_solution, clients, depot, vehicle_colors)
        pygame.display.flip()
        
        # Gera nova geração
        parents = select_parents(population, fitness_values, population_size // 2)
        new_population = []
        for i in range(0, len(parents), 2):
            if i + 1 < len(parents):
                child1, child2 = crossover(parents[i], parents[i + 1], clients, vehicle_capacity)
                child1 = mutate(child1, mutation_rate, clients, vehicle_capacity)
                child2 = mutate(child2, mutation_rate, clients, vehicle_capacity)
                new_population.extend([child1, child2])
        
        population = new_population[:population_size - 1] + [best_solution]
        generation += 1
        print(f"Geração {generation}: Melhor aptidão = {best_fitness}")
    
    print(f"Melhor solução: {best_solution}")
    print(f"Melhor aptidão: {best_fitness}")
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                running = False
    
    pygame.quit()

if __name__ == "__main__":
    main()