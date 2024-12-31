import pygame
from pygame.locals import *
import sys
import utils
from SimulationObject import SimulationObject
from Player import Player
import utils

BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 200, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BG_COLOR = GREEN
ROW_GAP = 50
COL_GAP = 80

class Drill:
    '''Manages the players in the drill and runs the pygame simulation.
    '''
    def __init__(self, num_lines: int = 4, num_players: int = 15, starting_line: int = 0, speed: int = 5):
        '''Constructs a drill.

        Args:
            num_lines (int, optional): Number of lines in the drill. Defaults to 4.
            num_players (int, optional): Total number of players in the drill. Defaults to 15.
            starting_line (int, optional): The index of the line that starts with the ball. Defaults to 0.
            player_speed (int, optional): The speed of the players in the drill. Defaults to 5.
        '''
        # Pygame attributes/setup
        pygame.init()
        self.fps = pygame.time.Clock()
        self.surface = pygame.display.set_mode((1000, 1000))
        pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP])
        self.players_moving = False # The player that is currently moving in the Pygame display
        self.ball_moving = False # The ball that is currently moving in the Pygame display
        
        # Drill attributes/setup
        assert num_lines < num_players + 1, "Number of lines must be less than number of players + 1"
        assert num_lines > 1, "Number of lines must be greater than 1"
        self.num_lines = num_lines
        self.num_players = num_players
        self.direction = 'right'
        self.starting_line = self.line_with_ball = starting_line
        self.speed = speed
        self.has_oscillators = False # Flag to check if any player has oscillated
        self.lines = [[] for _ in range(num_lines)]
        self.ball = SimulationObject('../assets/ball.png', 0, 0, speed)
        utils.tint_image(self.ball.image, WHITE)
        self.init_lines()
        
    def run(self, num_iterations: int = 10, verbose: bool = True):        
        '''Runs the drill simulation for a specified number of iterations.

        Args:
            num_iterations (int, optional): The number of iterations that the drill is run. Defaults to 10.
            verbose (bool, optional): Whether to print the drill state at each iteration. Defaults to True.
        '''
        iteration = 0
        while True:      
            if iteration > num_iterations:
                self.quit(num_iterations, verbose)
                
            key = pygame.key.get_pressed()
            if key[K_SPACE] or key[K_q]:
                self.quit(num_iterations, verbose)
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.quit(num_iterations, verbose)       
            
            if self.ball_moving:
                self.ball_moving = self.ball.move()
            elif self.players_moving:
                self.move_all_players()
            else:
                self.pass_ball(iteration)
                iteration += 1
                    
            self.surface.fill(BG_COLOR)            
            self.draw_all()
            pygame.display.update()
            self.fps.tick(30)
            
    def quit(self,  num_iterations: int = -1, verbose: bool = False):
        '''Quit the pygame simulation.

        Args:
            num_iterations (int, optional): The number of iterations in the drill has run for. Defaults to -1.
            verbose (bool, optional): True to print oscillation information; False otherwise. Defaults to False.
        '''
        if verbose:
            assert num_iterations > 0 , "Number of iterations must be greater than 0"
            self.print_oscillations(num_iterations)
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
                p = Player(
                    x=(col * COL_GAP + 100), 
                    y=(row * ROW_GAP + 100), 
                    player_id=pid, 
                    curr_line=col, 
                    speed=self.speed
                    )
                self.lines[col].append(p)
                pid += 1
                self.players.add(p)
        self.lines[self.starting_line][0].has_ball = True
        self.ball.rect.center = self.lines[self.starting_line][0].rect.center
        
    def draw_all(self):
        '''Draw all the simulation objects in the drill.
        '''
        self.players.draw(self.surface)
        self.ball.draw(self.surface)
        
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
        
        # set path for player to move to the target line in the lists
        target_x = self.lines[next_line][-1].rect.center[0]
        target_y = self.lines[next_line][-1].rect.center[1] + ROW_GAP
        player.set_path(target_x, target_y)
        
        # set the path for the ball to move in the Pygame display
        next_first = self.lines[next_line][0]
        ball_x, ball_y = next_first.rect.center[0], next_first.rect.center[1]
        self.ball.set_path(ball_x, ball_y)
        
        # move the player in the array representation of the drill
        player.has_ball = False
        self.lines[curr_line].pop(0)
        self.lines[next_line].append(player)
        self.lines[next_line][0].has_ball = True
        self.line_with_ball = next_line
                        
        # check if an oscillation has occurred
        if (not (curr_line == 0 or curr_line == self.num_lines - 1) and
            player.previous_line == next_line):
            if player.oscillation_count == 0:
                player.iteration_of_first_oscillation = curr_iteration

            self.has_oscillators = True
            player.oscillation_count += 1
            
        # update current and previous line of the moving player
        player.previous_line = player.curr_line
        player.curr_line = next_line
        
        # shift all the players in the previous line up
        for p in self.lines[curr_line]:
            p.set_path(p.rect.center[0], p.rect.center[1] - ROW_GAP)
        
        self.players_moving = True
        self.ball_moving = True
        
    def print_oscillations(self, total_iterations: int = 10):
        '''Print information on oscillations that occurred during the drill.

        Args:
            total_iterations (int, optional): The total number of iterations the drill was run. Defaults to 10.
        '''
        players = self.get_and_sort_players()
        for player in players:
            if player.oscillation_count > 0:
                percentage = player.oscillation_count / total_iterations * 100
                percentage_str = f'{percentage:.1f}'
                s = f"Player {player.id:>3} oscillated {player.oscillation_count:>4} times ({percentage_str:>5}% of the drill). Their first oscillation was on iteration {player.iteration_of_first_oscillation:>3}."
                
                utils.printRed(s) if percentage >= 2 else utils.printGreen(s)
            else:
                utils.printGreen(f"Player {player.id} did not oscillate.")

    def get_and_sort_players(self) -> list:
        '''Get all the players in the drill and sort them by id.

        Returns:
            list: A list of all the players in the drill sorted by id.
        '''
        players = []
        for line in self.lines:
            for player in line:
                players.append(player)
        players.sort(key=lambda x: x.id)
        return players
                
if __name__ == "__main__":
    drill = Drill(speed=10)
    drill.run(10)
