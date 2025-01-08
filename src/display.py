import pygame

from display_object import DisplayObject
from player import Player
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
        start_line: int,
        lines: list[list[Player]],
        speed: int, 
        win_size: tuple[int, int], 
        obj_tints: dict[int, RGB | RGBA],
        bg_color: RGB | RGBA,
        frame_rate: int, 
        step: bool,
        debug: bool,
    ):
        '''Constructor for Display class.

        Args:
            start_line (int): The line the ball starts on.
            lines (list[list[Player]]): A list of lines with players.
            speed (int): The rate at which sprites move.
            win_size (tuple[int, int]): The size of the window.
            obj_tints (dict[int, RGB  |  RGBA]): A dictionary of player ids and their respective tints if any. Empty dict will result in using default png colors.
            bg_color (RGB | RGBA): The background color of the window.
            frame_rate (int): The frame rate of the simulation.
            step (bool): Whether to run the simulation in step mode. This will pause the simulation after each pass. User must press space to continue.
            debug (bool): Whether to display the id of players instead of the image.
        '''
        self.verify_obj_tints(obj_tints)
        
        pygame.init()
        pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP])
        self.clock = pygame.time.Clock()
        self.win = pygame.display.set_mode(win_size)
        self.speed = speed
        self.frame_rate = frame_rate
        self.step = step
        
        self.lines = lines
        self.start_line = start_line
        self.players, self.player_dict, self.ball = self._init_objects(obj_tints)
        self.ball_moving = False
        self.moving_players = set()
        self.bg = bg_color
        self.debug = debug
    
    def update(self) -> bool:
        '''Perform one pass of the simulation, moving all game_objects 
        until they complete their paths. 

        Returns:
            bool: True if the update successfully completes, False otherwise.
        '''
        if self.step:
            start = False
            while not start:
                for event in pygame.event.get():
                    start = event.type == KEYDOWN and event.key == K_SPACE
                    break
                    
        
        while self.ball_moving or len(self.moving_players) > 0:
            dt = self.clock.tick(self.frame_rate) / 1000
            adjusted_speed = self.speed * dt
            
            if self.check_exit_conditions():
                self.close()
                return False
            
            if self.ball_moving:
                self.ball_moving = self.ball.update(adjusted_speed)
            else:
                to_remove = set()
                
                # move all players that need to be moved
                for p in self.moving_players:
                    still_moving = p.update(adjusted_speed)
                    
                    if not still_moving:
                        to_remove.add(p)
                
                # remove all players that have completed their paths
                self.moving_players = self.moving_players - to_remove
            
            self.win.fill(self.bg)
            
            # draw all players
            for p in self.players:
                p.draw(self.win, self.debug)
            self.ball.draw(self.win)
            
            pygame.display.flip()
            
        return True
    
    def pass_ball(self, curr_line: int, target_line: int): 
        '''Sets paths of ball and players for one pass from 
        curr_line to target_line. 
        
        **IMPORTANT** This function assumes that 
        the players have not yet been moved in the Drill object. 
        Always move players to next line after calling this function.

        Args:
            curr_line (int): The line the ball is currently on.
            target_line (int): The line the ball is passing to.
        '''
        # set the path of the ball
        # 
        # LOGIC: get the id of the first player in the target line from drill object 
        # and find the corresponding sprite in the player_dict. Use that sprite's 
        # center as the target.
        ball_target = self.player_dict[self.get_id(target_line)].rect.center
        self.ball.set_path(*ball_target)
        self.ball_moving = True
        
        # set the path of the passing player
        # 
        # LOGIC: get id of last player in target line from drill object and find 
        # corresponding sprite in player_dict. Since the player is going behind 
        # the last player in the target line, add ROW_GAP to the y coordinate.
        player_target_x, player_target_y = self.player_dict[self.get_id(target_line, first=False)].rect.center
        player_target_y += ROW_GAP
        moving_player = self.player_dict[self.get_id(curr_line)]
        moving_player.set_path(player_target_x, player_target_y)
        self.moving_players.add(moving_player)
        
        # set the path for shifting the rest of the players in the current line
        for i in range(1, len(self.lines[curr_line])):
            # get the player from the player_dict using id from drill object
            player_id = self.lines[curr_line][i].id
            player = self.player_dict[player_id]
            
            # set target location to one row above the player's current location
            player_target_x, player_target_y = player.rect.center
            player_target_y -= ROW_GAP
            
            # set path
            player.set_path(player_target_x, player_target_y)
            
            # add player to set of moving players
            self.moving_players.add(player)
        
    def _init_objects(
        self, 
        obj_tints: dict[int, RGB | RGBA]
    ) -> tuple[set[DisplayObject], dict[int, DisplayObject], DisplayObject]:
        '''Create all the game objects for the simulation. A variable 
        number of players and one ball.

        Args:
            obj_tints (dict[int, RGB  |  RGBA]): The tints of the players. This can be empty
            which will result in using the default png colors.

        Returns:
            tuple[list[DisplayObject], dict[int, DisplayObject], DisplayObject]: A list of players, a dict that keeps track of each player's pid, and the ball.
        '''
        player_dict = {}
        players = pygame.sprite.Group()
        col_counter = 0
                
        # ----
        for col, line in enumerate(self.lines):
            for row, player in enumerate(line):
                pid = player.id
                
                # initialize player
                p = DisplayObject(
                    '../assets/player.png',
                    col * COL_GAP + 100,
                    row * ROW_GAP + 100, 
                    pid
                )
                
                # set player tint
                if pid in obj_tints.keys():
                    p.set_tint(obj_tints[pid])
                else:
                    # rotate players colors for enhanced visibility
                    if col_counter == 0:
                        p_color = 'darkslategray'
                    else:
                        p_color = f'darkslategray{col_counter}'
                    col_counter +=1 
                    col_counter %= 4
                    
                    p.set_tint(pygame.colordict.THECOLORS[p_color])
                    
                # add player to the correct line and the group of players
                player_dict[pid] = p
                players.add(p)
        
        # initialize ball
        ball_x, ball_y = player_dict[self.get_id(self.start_line)].rect.center
        ball = DisplayObject('../assets/ball.png', ball_x, ball_y, -1)
        if -1 in obj_tints.keys():
            ball.set_tint(obj_tints[-1])
        
        return players, player_dict, ball
    
    def get_id(self, line_index: int, first: bool = True) -> int:
        '''Get the player id of the first or last player in a line.

        Args:
            line_index (int): The index of the line.
            first (bool, optional): True if the first player id is needed, 
            False if the last player id is needed. Defaults to True.

        Returns:
            int: The player id.
        '''
        if first:
            return self.lines[line_index][0].id
        else:
            return self.lines[line_index][-1].id
        
    def check_exit_conditions(self) -> bool:
        '''Checks if any of the following exit condiitons are fulfilled:
            - The user has pressed the space bar or 'q' key to exit the simulation.
            - The user has clicked the close button on the pygame window.
            
        Returns:
            bool: True if any of the exit conditions are fulfilled, False otherwise.
        '''
        key = pygame.key.get_pressed()
        if key[K_q]:
            pygame.event.post(pygame.event.Event(QUIT))
        
        for event in pygame.event.get():
            if event.type == QUIT:
                return True
        
        return False
    
    def verify_obj_tints(self, obj_tints: dict[int, RGB | RGBA | str]):
        '''Verify that the obj_tints dictionary is correctly formatted. It 
        must contain integer keys and values that are either RGB, RGBA, or
        a valid color name from pygame.colordict.THECOLORS. The keys must 
        be found in the player_dict or be -1 for the ball.

        Args:
            obj_tints (dict[int, RGB  |  RGBA  |  str]): The dictionary of object tints.
        '''
        if not obj_tints:
            return
        
        for k, v in obj_tints.items():
            assert isinstance(k, int), f"ID must be an integer. Got {k} instead."
            
            if isinstance(v, list):
                assert len(v) in [3, 4], f"Must be RGB or RGBA. Got {v} instead."
                for i in v:
                    assert isinstance(i, int) and i in range(256), f"Must be valid RGB or RGBA. Got {v} instead."
                obj_tints[k] = tuple(v)
            elif isinstance(v, str):
                assert v in pygame.colordict.THECOLORS, f"Must be a valid color name from pygame.colordict.THECOLORS. Got {v} instead."
                obj_tints[k] = pygame.colordict.THECOLORS[v]
            elif isinstance(v, tuple):
                assert len(v) in [3, 4], f"Must be RGB or RGBA. Got {v} instead."
                for i in v:
                    assert isinstance(i, int) and i in range(256), f"Must be valid RGB or RGBA. Got {v} instead."
            else:
                raise AssertionError(f"Value must be a list or string. Got {v} instead.")
        
    def close(self):
        pygame.quit()