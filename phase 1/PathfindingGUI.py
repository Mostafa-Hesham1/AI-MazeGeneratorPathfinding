import pygame
from config import *




class PathfindingGUI:
    def __init__(self, maze_obstacles, start_pos, goal_pos):
        pygame.init()
        self.screen = pygame.display.set_mode((GRID_SIZE * CELL_SIZE + 150, GRID_SIZE * CELL_SIZE))
        pygame.display.set_caption("Maze Pathfinding")
        self.clock = pygame.time.Clock()

        self.maze_obstacles = maze_obstacles
        self.start_pos = start_pos
        self.goal_pos = goal_pos

        self.dfs_button = pygame.Rect(10, 50, 130, 30)
        self.bfs_button = pygame.Rect(10, 100, 130, 30)
        self.astar_button = pygame.Rect(10, 150, 130, 30)

        self.running = True
        self.draw()

    def draw_buttons(self):

    def draw_maze(self):
    def draw_path(self, path):
        print("Drawing path:", path)
        for pos in path:
            print("Position:", pos)
            x, y = pos
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(self.screen, (255, 0, 0), rect) 
    def run_search_algorithm(self, algorithm):
        if algorithm == 'dfs':
            path = dfs(self.maze_obstacles, self.start_pos, self.goal_pos)
        elif algorithm == 'bfs':
            path = bfs(self.maze_obstacles, self.start_pos, self.goal_pos)
        elif algorithm == 'astar':
            path = a_star(self.maze_obstacles, self.start_pos, self.goal_pos)
        self.draw_path(path)

    def draw(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.dfs_button.collidepoint(event.pos):
                        self.run_search_algorithm('dfs')
                    elif self.bfs_button.collidepoint(event.pos):
                        self.run_search_algorithm('bfs')
                    elif self.astar_button.collidepoint(event.pos):
                        self.run_search_algorithm('astar')

            self.screen.fill(WHITE)
            self.draw_maze()
            self.draw_buttons()
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()
