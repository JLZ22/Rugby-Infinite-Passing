import pygame
from pygame.locals import *
import sys

BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 200, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BG_COLOR = GREEN
ROW_GAP = 60
COL_GAP = 150

class Player(pygame.sprite.Sprite):
    '''A player in the drill.

    Args:
        pygame (Sprite): A sprite object from pygame.
    '''
    def __init__(self, x: int, y: int, curr_line: int, player_id: int):
        '''Constructs a player.

        Args:
            x (int): starting x location
            y (int): starting y location
            curr_line (int): index of the line the player is in
            player_id (int): unique id of the player
        '''
        super().__init__()
        
        # Game attributes
        img = pygame.image.load("../assets/player.png").convert_alpha()
        self.image = pygame.transform.scale(img, (50, 50))  
        self.rect = self.image.get_rect()
        self.rect.center=(x,y) 
        self.curr_line = curr_line
        
        # Player attributes
        self.id = player_id
        self.has_ball = False
        self.previous_line = -1
        self.oscillation_count = 0
        self.iteration_of_first_oscillation = -1
        self.target = (x, y)
        self.path = []
        self.speed = 5

    def set_path(self,target_x, target_y, split_ratio=0.5):
        """Define a path that moves right, then down, then right again."""
        start_x = self.rect.center[0]
        start_y = self.rect.center[1]
        
        delta_x = target_x - start_x
        delta_y = target_y - start_y

        # Split horizontal movement
        right1_distance = delta_x * split_ratio

        # Generate path
        self.path = [
            (start_x + right1_distance, start_y),  # First right
            (start_x + right1_distance, start_y + delta_y),  # Down
            (target_x, target_y),  # Second right
        ]
        self.target = self.path.pop(0)

    def move(self):
        """Move toward the current target."""
        if not self.target:
            return False  # No target, movement complete

        target_x, target_y = self.target
        current_x, current_y = self.rect.center

        # Calculate movement step
        dx = target_x - current_x
        dy = target_y - current_y
        distance = (dx**2 + dy**2) ** 0.5

        if distance <= self.speed:
            self.rect.center = self.target
            if self.path:
                self.target = self.path.pop(0)
            else:
                self.target = None
        else:
            step_x = self.speed * (dx / distance)
            step_y = self.speed * (dy / distance)
            self.rect.move_ip(step_x, step_y)

        return True  # Still moving
        
    def draw(self, display: pygame.Surface):
        '''Draw the player on the display.

        Args:
            display (pygame.Surface): The display to draw the player on.
        '''
        display.blit(self.image, self.rect)
        
class Drill:
    '''Manages the players in the drill and runs the pygame simulation.
    '''
    
    def __init__(self, num_lines: int = 4, num_players: int = 15, starting_line: int = 0):
        '''Constructs a drill.

        Args:
            num_lines (int, optional): Number of lines in the drill. Defaults to 4.
            num_players (int, optional): Total number of players in the drill. Defaults to 15.
            starting_line (int, optional): The index of the line that starts with the ball. Defaults to 0.
        '''
        # Pygame setup
        pygame.init()
        self.fps = pygame.time.Clock()
        self.surface = pygame.display.set_mode((1000, 1000))
        pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP])
        
        # Drill attributes/setup
        assert num_lines < num_players + 1, "Number of lines must be less than number of players + 1"
        assert num_lines > 1, "Number of lines must be greater than 1"
        self.num_lines = num_lines
        self.num_players = num_players
        self.direction = 'right'
        self.starting_line = starting_line # The line that starts with the ball
        self.line_with_ball = starting_line # The line that has the ball
        self.lines = [[] for _ in range(num_lines)] # array of lines
        self.has_oscillators = False
        self.players_moving = False # The player that is currently moving
        self.init_lines()
        
    def run(self, num_iterations: int = 10):        
        '''Runs the drill simulation for a specified number of iterations.

        Args:
            num_iterations (int, optional): The number of iterations that the drill is run. Defaults to 10.
        '''
        iteration = 0
        while True:      
            if iteration >= num_iterations:
                self.quit()
                
            key = pygame.key.get_pressed()
            if key[K_SPACE] or key[K_q]:
                self.quit()
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.quit()       
            
            if self.players_moving:
                self.move_all_players()
            else:
                self.pass_ball(iteration)
                iteration += 1
                    
            self.surface.fill(BG_COLOR)            
            self.draw_all_players()
            pygame.display.update()
            self.fps.tick(30)
            
    def quit(self):
        '''Quit the pygame simulation and exit the program.
        '''
        pygame.quit()
        sys.exit()
    
    def init_lines(self):
        '''Instantiate the players and distribute them into lines from left to right.
        '''
        self.players = pygame.sprite.Group()
        pid = 1 # 1 indexed player id
        num_rows = self.num_players // self.num_lines
        
        for col in range(self.num_lines):
            for row in range(num_rows + 1):
                if (pid > self.num_players):
                    break
                p = Player(col * COL_GAP + 100, row * ROW_GAP + 100, col, pid)
                self.lines[col].append(p)
                pid += 1
                self.players.add(p)
        self.lines[self.starting_line][0].has_ball = True
        
    def draw_all_players(self):
        '''Draw all the players in the drill.
        '''
        self.players.draw(self.surface)
        
    def move_all_players(self):
        '''Move all the players in the drill.
        '''
        moving = False
        for player in self.players:
            still_moving = player.move()
            if still_moving:
                moving = True
                
        self.players_moving = moving
                
    def is_last_line(self):
        '''Check if the line with the ball is in one of the last lines.
        '''
        if self.direction == 'left':
            return self.line_with_ball == 0
        else:
            return self.line_with_ball == self.num_lines - 1
        
    def flip_direction(self):
        '''Flip the direction of the drill.
        '''
        if self.direction == 'left':
            self.direction = 'right'
        else:
            self.direction = 'left'
            
    def pass_ball(self, iteration: int):
        '''Pass the ball to the next line.

        Args:
            iteration (int): The current iteration of the drill.
        '''
        if self.is_last_line():
            self.flip_direction()

        if self.direction == 'left':
            self.move_player_to_next_line(self.line_with_ball, self.line_with_ball - 1, iteration)
        else:
            self.move_player_to_next_line(self.line_with_ball, self.line_with_ball + 1, iteration)
            
    def move_player_to_next_line(self, curr_line: int, next_line: int, curr_iteration: int):
        '''Move the first player in the current line to the end of the next line 
        based on the direction of the drill.

        Args:
            curr_line (int): The index of the current line.
            next_line (int): The index of the next line.
            curr_iteration (int): The current iteration of the drill.
        '''
        assert self.lines[next_line], f"Line {next_line + 1} is empty! Player in line {curr_line + 1} is passing to no one!"
        assert self.lines[curr_line], f"Line {curr_line + 1} is empty! Player in line {next_line + 1} is recieving from no one!"
        assert next_line != curr_line, "Player cannot pass to their current line!"
        
        player = self.lines[curr_line][0]
        direction = 'right' if next_line > curr_line else 'left'
        
        # set the path for the player to move 
        target_x = self.lines[next_line][-1].rect.center[0]
        target_y = self.lines[next_line][-1].rect.center[1] + ROW_GAP
        player.set_path(target_x, target_y)
        
        # move the player to the target line in the lists
        player.has_ball = False
        self.lines[curr_line].pop(0)
        self.lines[next_line].append(player)
        self.lines[next_line][0].has_ball = True
        self.line_with_ball = next_line
        
                        
        # check if an oscillation has occurred
        if (not (curr_line == 0 or curr_line == self.num_lines - 1) and
            player.previous_line == next_line):
            if player.oscillationCount == 0:
                player.iteration_of_first_oscillation = curr_iteration

            self.has_oscillators = True
            player.oscillationCount += 1
            
        # update current and previous line of the moving player
        player.previous_line = player.curr_line
        player.curr_line += 1 if direction == 'right' else -1
        
        # shift all the players in the previous line up
        for p in self.lines[curr_line]:
            p.set_path(p.rect.center[0], p.rect.center[1] - ROW_GAP)
        
        self.players_moving = True
                
if __name__ == "__main__":
    drill = Drill()
    drill.run()