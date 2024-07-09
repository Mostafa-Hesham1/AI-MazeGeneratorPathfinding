import pygame
import sys
import time  
from collections import deque
from queue import PriorityQueue

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GREY = (220, 220, 220)
CELL_SIZE = 20
GRID_SIZE = 25
DIRECTIONS = [(0, -1), (1, 0), (0, 1), (-1, 0)]
YELLOW = (255, 255, 0)

def is_valid_position(pos, obstacles):
    x, y = pos
    return 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE and pos not in obstacles

class MazeGUI:
    def __init__(self):
        pygame.init()
        self.delay_ms = 100  

        self.screen = pygame.display.set_mode((GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE + 50))
        pygame.display.set_caption("Maze Builder")
        self.clock = pygame.time.Clock()

        self.maze_obstacles = set()
        self.agent_start_pos = None
        self.prize_pos = None
        self.algorithm_text = ""
        self.algorithm_running = False
        self.algorithm_step = 0
        self.algorithm_path = []
        self.stack = []
        self.visited = set()
        self.path = {}
        self.running = True
        self.final_path = []  
        self.left_mouse_button_down = False 

        self.dfs_button = pygame.Rect(10, GRID_SIZE * CELL_SIZE + 10, 80, 30)
        self.bfs_button = pygame.Rect(100, GRID_SIZE * CELL_SIZE + 10, 80, 30)
        self.astar_button = pygame.Rect(190, GRID_SIZE * CELL_SIZE + 10, 80, 30)
        self.screen.fill(WHITE)  
        self.clear_button = pygame.Rect(280, GRID_SIZE * CELL_SIZE + 10, 80, 30)

        self.draw()

    def start_pathfinding(self, algorithm):
        if self.agent_start_pos and self.prize_pos:
            self.algorithm_running = True
            self.algorithm_step = 0
            self.algorithm_path = []
            self.algorithm_text = algorithm.lower()
            self.visited = {self.agent_start_pos}
            self.path = {}
            self.final_path = []

            if self.algorithm_text == 'dfs':
                self.stack = [self.agent_start_pos]
            elif self.algorithm_text == 'bfs':
                self.queue = deque([self.agent_start_pos])
            elif self.algorithm_text == 'astar':
                self.pq = PriorityQueue()
                self.pq.put((0, self.agent_start_pos))
                self.g_values = {self.agent_start_pos: 0}


    def dfs_algorithm_step(self):
        if not self.stack:
            self.algorithm_running = False
            return

        current = self.stack[-1]  
        if current == self.prize_pos:
            self.final_path = self.compute_final_path()  
            self.algorithm_running = False  
            return

        self.visited.add(current)
        self.algorithm_path.append(current) 

        neighbors_explored = False
        for dx, dy in DIRECTIONS:
            next_pos = (current[0] + dx, current[1] + dy)
            if is_valid_position(next_pos, self.maze_obstacles) and next_pos not in self.visited:
                self.stack.append(next_pos)
                self.path[next_pos] = current
                neighbors_explored = True
                break

        if not neighbors_explored:
            self.stack.pop() 

    def bfs_algorithm_step(self):
        if not self.queue:
            self.algorithm_running = False
            return

        current = self.queue.popleft()
        self.algorithm_path.append(current)

        if current == self.prize_pos:
            self.final_path = self.backtrack_path(self.path)  
            self.algorithm_running = False
            return

        for dx, dy in DIRECTIONS:
            next_pos = (current[0] + dx, current[1] + dy)
            if is_valid_position(next_pos, self.maze_obstacles) and next_pos not in self.visited:
                self.queue.append(next_pos)
                self.path[next_pos] = current
                self.visited.add(next_pos)
    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def a_star_algorithm_step(self):
        if self.pq.empty():
            self.algorithm_running = False
            return

        current_cost, current = self.pq.get()
        self.algorithm_path.append(current)

        if current == self.prize_pos:
            self.final_path = self.backtrack_path(self.path) 
            self.algorithm_running = False
            return

        for dx, dy in DIRECTIONS:
            next_pos = (current[0] + dx, current[1] + dy)
            new_cost = self.g_values.get(current, float('inf')) + 1
            if is_valid_position(next_pos, self.maze_obstacles) and (next_pos not in self.g_values or new_cost < self.g_values[next_pos]):
                self.g_values[next_pos] = new_cost
                f_value = new_cost + self.heuristic(self.prize_pos, next_pos)
                self.pq.put((f_value, next_pos))
                self.path[next_pos] = current

    def backtrack_path(self, path):
        final_path = []
        current = self.prize_pos
        while current != self.agent_start_pos:
            final_path.append(current)
            current = path[current]
        final_path.append(self.agent_start_pos)
        final_path.reverse()
        return final_path 
    
    def compute_final_path(self):
        final_path = []
        current = self.prize_pos
        while current != self.agent_start_pos:
            final_path.append(current)
            current = self.path[current]
        final_path.append(self.agent_start_pos)
        final_path.reverse()
        return final_path
        return path or []


    def visualize_algorithm(self):
        for position in self.algorithm_path:
            rect = pygame.Rect(position[0] * CELL_SIZE, position[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(self.screen, RED, rect)

        for position in self.final_path:
            rect = pygame.Rect(position[0] * CELL_SIZE, position[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(self.screen, YELLOW, rect)

        if self.algorithm_path:
            self.algorithm_path.pop(0) 

    def draw_grid(self):
        for x in range(0, GRID_SIZE * CELL_SIZE, CELL_SIZE):
            for y in range(0, GRID_SIZE * CELL_SIZE, CELL_SIZE):
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, GREY, rect, 1)

    def draw_obstacles(self):
        for obstacle in self.maze_obstacles:
            x, y = obstacle
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(self.screen, BLACK, rect)

    def draw_special_points(self):
        if self.agent_start_pos:
            x, y = self.agent_start_pos
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(self.screen, BLUE, rect)
        if self.prize_pos:
            x, y = self.prize_pos
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(self.screen, GREEN, rect)

    def draw_button(self):
        pygame.draw.rect(self.screen, GREY, self.dfs_button)
        pygame.draw.rect(self.screen, GREY, self.bfs_button)
        pygame.draw.rect(self.screen, GREY, self.astar_button)
        pygame.draw.rect(self.screen, GREY, self.clear_button)  
        font = pygame.font.SysFont(None, 24)
        dfs_text = font.render('DFS', True, BLACK)
        bfs_text = font.render('BFS', True, BLACK)
        astar_text = font.render('A*', True, BLACK)
        clear_text = font.render('Clear', True, BLACK) 

        dfs_text_rect = dfs_text.get_rect(center=self.dfs_button.center)
        bfs_text_rect = bfs_text.get_rect(center=self.bfs_button.center)
        astar_text_rect = astar_text.get_rect(center=self.astar_button.center)
        clear_text_rect = clear_text.get_rect(center=self.clear_button.center) 

        self.screen.blit(dfs_text, dfs_text_rect)
        self.screen.blit(bfs_text, bfs_text_rect)
        self.screen.blit(astar_text, astar_text_rect)
        self.screen.blit(clear_text, clear_text_rect)
    
    def clear_elements(self):
        self.maze_obstacles.clear()
        self.screen.fill(WHITE)  

        self.agent_start_pos = None
        self.prize_pos = None
        self.algorithm_text = ""
        self.algorithm_running = False
        self.algorithm_step = 0
        self.algorithm_path = []
        self.stack = []
        self.visited = set()
        self.path = {}
        self.final_path = []

    def update_screen(self):
        self.draw_grid()
        self.draw_obstacles()
        self.draw_special_points()
        self.draw_button()

        if self.algorithm_running:
            self.visualize_algorithm()

        for position in self.final_path:
            rect = pygame.Rect(position[0] * CELL_SIZE, position[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(self.screen, YELLOW, rect)

        pygame.display.flip()
        self.clock.tick(10)


    def draw(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: 
                        self.left_mouse_button_down = True

                    if self.dfs_button.collidepoint(event.pos):
                        self.start_pathfinding("dfs")
                    elif self.bfs_button.collidepoint(event.pos):
                        self.start_pathfinding("bfs")
                    elif self.astar_button.collidepoint(event.pos):
                        self.start_pathfinding("astar")
                    elif self.clear_button.collidepoint(event.pos):
                        self.clear_elements()
                    else:
                        x, y = event.pos
                        grid_x, grid_y = x // CELL_SIZE, y // CELL_SIZE
                        if grid_y < GRID_SIZE: 
                            if event.button == 1: 
                                if (grid_x, grid_y) not in self.maze_obstacles:
                                    self.maze_obstacles.add((grid_x, grid_y))
                                else:
                                    self.maze_obstacles.remove((grid_x, grid_y))
                            elif event.button == 3: 
                                if not self.agent_start_pos:
                                    self.agent_start_pos = (grid_x, grid_y)
                                elif not self.prize_pos:
                                    self.prize_pos = (grid_x, grid_y)

                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1: 
                        self.left_mouse_button_down = False

                elif event.type == pygame.MOUSEMOTION:
                    if self.left_mouse_button_down:
                        x, y = event.pos
                        grid_x, grid_y = x // CELL_SIZE, y // CELL_SIZE
                        if grid_y < GRID_SIZE and (grid_x, grid_y) not in self.maze_obstacles:
                            self.maze_obstacles.add((grid_x, grid_y))

            if self.algorithm_running:
                if self.algorithm_text == 'dfs':
                    self.dfs_algorithm_step()
                elif self.algorithm_text == 'bfs':
                    self.bfs_algorithm_step()
                elif self.algorithm_text == 'astar':
                    self.a_star_algorithm_step()

            self.update_screen()


if __name__ == "__main__":
    MazeGUI()
