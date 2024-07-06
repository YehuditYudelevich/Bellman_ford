import pygame
import sys

pygame.init()
WIDTH, HEIGHT = 1500, 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bellman-Ford")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
YELLOW = (255, 255, 0)

graf = {
    'A': {'B': -1, 'C': 4},
    'B': {'D': -1, 'F': 10, 'C': 3},
    'C': {'G': 5, 'F': -2},
    'D': {'E': 2},
    'E': {'B': 7, 'I': 2, 'F': 3},
    'F': {'I': -4, 'H': 1},
    'G': {'H': -2},
    'H': {'I': 2},
    'I': {}
}

node_positions = {
    'A': (200, 100),
    'B': (500, 100),
    'C': (400, 350),
    'D': (700, 50),
    'E': (900, 200),
    'F': (600, 500),
    'G': (400, 650),
    'H': (800, 650),
    'I': (1000, 500)
}

def draw_graph(current, distances, checked=None):
    screen.fill(BLACK)
    pygame.draw.circle(screen, YELLOW, (20,555), 10)
    pygame.draw.circle(screen,GREEN,(20,585),10)
    pygame.draw.circle(screen,RED,(20,615),10)
    font=pygame.font.Font(None,25)
    text=font.render("Yellow marks the source vertex",True,WHITE)
    screen.blit(text,(35,550))
    text=font.render("Green marks all nodes",True,WHITE)
    screen.blit(text,(35,580))
    text=font.render("Red marks the current",True,WHITE)
    screen.blit(text,(35,610))
    for node, neighbors in graf.items():
        for neighbor, weight in neighbors.items():
            start_pos = node_positions[node]
            end_pos = node_positions[neighbor]
            pygame.draw.line(screen, GRAY, start_pos, end_pos, 6)
            mid_x = (start_pos[0] + end_pos[0]) // 2
            mid_y = (start_pos[1] + end_pos[1]) // 2
            font = pygame.font.Font(None, 25)
            text = font.render(str(weight), True, WHITE)
            screen.blit(text, (mid_x + 20, mid_y - 20))

    for node, pos in node_positions.items():
        color = GREEN
        if node == current:
            color = YELLOW
        if node == checked:
            color = RED
        pygame.draw.circle(screen, color, pos, 22)
        font = pygame.font.Font(None, 25)
        text = font.render(str(node), True, BLACK)
        screen.blit(text, ((pos[0] -8, pos[1] - 10)))
        
        distance = distances.get(node, float("inf"))
        if distance < float("inf"):
            dist_next = font.render(str(distance), True, WHITE)
            pygame.draw.rect(screen,BLUE,(pos[0]-15,pos[1]+23,25,25))
            screen.blit(dist_next, (pos[0] -10, pos[1] + 25))
            
            start_x,start_y=880,70
            padding = 4
            font=pygame.font.Font(None,28)
            text=font.render("The array contain the distances from A to the all vertex",True,WHITE)
            screen.blit(text,(start_x,start_y-50))
            keys = list(graf.keys())
            for i, node in enumerate(keys):
                x = start_x + i * (60 + padding)
                pygame.draw.rect(screen, YELLOW, (x,start_y, 60, 50))
                font=pygame.font.Font(None,25)
                text = font.render(f"{node}: {distances[node] if distances[node] < float('inf') else 'inf'}", True, BLACK)
                screen.blit(text,(x+5,start_y+15))
                
    pygame.display.flip()

def belman_ford(start):
    distances = {node: float("inf") for node in graf}
    distances[start] = 0
    
    for _ in range(len(graf) - 1):
        for node in graf:
            for neighbor, weight in graf[node].items():
                if distances[node] + weight < distances[neighbor]:
                    distances[neighbor] = distances[node] + weight
                    draw_graph(start, distances, checked=neighbor)
                    pygame.time.wait(10000)
    return distances

running = True
current = 'A'
distances = belman_ford(current)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    draw_graph(current, distances)
    pygame.display.flip()
pygame.quit()
sys.exit()
