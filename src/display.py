import pygame

from drill import Drill
from display_object import DisplayObject
from pygame.locals import *

RGB = tuple[int, int, int]
RGBA = tuple[int, int, int, int]
COL_GAP =  80
ROW_GAP = 50

class Display():
    '''The display class for the simulation. 
    This class is responsible for visualizing the drill.
    '''
    
    def __init__(
        self, 
        drill: Drill, 
        speed: int, 
        win_size: tuple[int, int], 
        player_tints: dict[int, RGB | RGBA],
        ball_tint: RGB | RGBA,
        bg_color: RGB | RGBA,
        frame_rate: int, 
    ):
        '''Constructor for Display class.

        Args:
            drill (Drill): The backend that this display is visualizing.
            speed (int): The rate at which sprites move.
            win_size (tuple[int, int]): The size of the window.
            player_tints (dict[int, RGB  |  RGBA]): A dictionary of player ids and their respective tints if any. Empty dict will result in using default png colors.
            ball_tint (RGB | RGBA): The tint of the ball. None will result in using default png color.
            bg_color (RGB | RGBA): The background color of the window.
            frame_rate (int): The frame rate of the simulation.
        '''
        pygame.init()
        pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP])
        self.clock = pygame.time.Clock()
        self.win = pygame.display.set_mode(win_size)
        self.drill = drill
        self.speed = speed
        self.players, self.ball = self.init_objects(player_tints, ball_tint)
        self.frame_rate = frame_rate
        self.ball_moving = False
        self.players_moving = False
        self.moving_players = set()
        self.bg = bg_color
    
    async def update(self) -> bool:
        while self.ball_moving or self.players_moving:
            dt = self.clock.tick(self.frame_rate) / 1000
            adjusted_speed = self.speed * dt
            
            if self.check_exit_conditions():
                pygame.quit()
                return False
            
            if self.ball_moving:
                self.ball_moving = self.ball.update(adjusted_speed)
            elif self.players_moving:
                # move all players that need to be moved
                for p in self.moving_players:
                    still_moving = p.update(adjusted_speed)
                    
                    # if the player is no longer moving, remove them from the moving players set
                    if not still_moving:
                        self.moving_players.remove(p)
                
                # if there are no more moving players, set players_moving to False
                self.players_moving = len(self.moving_players) != 0
            
            self.win.fill(self.bg)
            
            # draw all players
            self.players.draw(self.win)
            self.ball.draw(self.win)
            
            pygame.display.flip()
            
        return True
        
    def init_objects(
        self, 
        player_tints: dict[int, RGB | RGBA], 
        ball_tint: RGB | RGBA | None
    ) -> tuple[list[DisplayObject], DisplayObject]:
        lines = [[] for _ in range(self.drill.num_lines)]
        players = pygame.sprite.Group()
        
        pid = 0
        num_rows = self.drill.num_players // self.drill.num_lines
        
        for row in range(num_rows):
            for col in range(self.drill.num_lines):
                # check that we don't add more players than are in the drill
                if pid >= self.drill.num_players:
                    break
                
                # initialize player
                p = DisplayObject(
                    '../assets/player.png',
                    x=col * COL_GAP + 100,
                    y=row * ROW_GAP + 100,
                )
                
                # set player tint
                if pid in player_tints.keys():
                    p.set_tint(player_tints[pid])
                    
                # add player to the correct line and the group of players
                lines[col].append(p)
                players.add(p)
                
                pid += 1
        
        # initialize ball
        ball_x, ball_y = lines[self.drill.start_line][0].rect.center
        ball = DisplayObject('../assets/ball.png', ball_x, ball_y)
        ball.set_tint(ball_tint)
        
        return players, ball
        
    def check_exit_conditions(self) -> bool:
        '''Checks if any of the following exit condiitons are fulfilled:
            - The user has pressed the space bar or 'q' key to exit the simulation.
            - The user has clicked the close button on the pygame window.
            
        Returns:
            bool: True if any of the exit conditions are fulfilled, False otherwise.
        '''
        key = pygame.key.get_pressed()
        if key[K_SPACE] or key[K_q]:
            pygame.event.post(pygame.event.Event(QUIT))
        
        for event in pygame.event.get():
            if event.type == QUIT:
                return True
        
        return False
    
    def close(self):
        pygame.quit()