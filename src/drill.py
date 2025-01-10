import math
import utils

from player import Player
from display import Display

class Drill:
    '''Manages the players in the drill and runs the pygame simulation.
    '''
    def __init__(
        self, 
        num_lines: int = 4, 
        num_players: int = 15, 
        starting_line: int = 0, 
        direction: str = 'right',
        line_config: dict[int, int] | None = None,
    ):
        '''Constructs a drill. Note that the number of lines must be 
        less than the number of players, the starting line must have 
        at least two players, and the starting line must be less than 
        number of lines. If the line_config is provided, num_lines and 
        num_players will be ignored. Starting line will be ignored if 
        it is provided in the line_config.

        Args:
            num_lines (int, optional): Number of lines in the drill. Defaults to 4.
            num_players (int, optional): Total number of players in the drill. Defaults to 15.
            starting_line (int, optional): The index of the line that starts with the ball. Defaults to 0.
            direction (str, optional): The direction of the drill. Defaults to 'right'.
            line_config (dict[int, int] | None, optional): A dictionary where the key is the line id and the value 
            is the number of players in that line. Defaults to None.
        '''
        assert num_lines < num_players + 1, "Number of lines must be less than number of players + 1"
        assert num_lines > 1, "Number of lines must be greater than 1"
        assert direction in ['left', 'right'], "Direction must be 'left' or 'right'."
        self.verify_line_config(line_config)
        
        self.starting_line = self.line_with_ball = starting_line
        self.moving_players = set() # List of players whose paths have been changed
        self.has_oscillators = False # Flag to check if any player has oscillated
        self.direction = direction
        
        if line_config:
            init_result = self._init_lines_from_config(line_config)
            self.num_lines = init_result[0]
            self.num_players = init_result[1]
            self.lines = init_result[2]
            self.players = init_result[3]
        else:
            self.num_lines = num_lines
            self.num_players = num_players
            self.lines, self.players = self._init_lines_default()
            
        
        assert len(self.lines[self.starting_line]) > 1, "Starting line must have more than one player."
        assert self.starting_line < self.num_lines, "Starting line must be less than number of lines."
        
    def run_visible(
        self, 
        total_passes: int, 
        display: Display,
        verbose: bool,
    ) -> int:
        '''Run the drill with the pygame simulation.

        Args:
            total_passes (int): The number of passes the drill is run for.
            speed (int): The speed of the players in the drill.
            display (Display): The display object for the simulation.
            verbose (bool): Whether to print information on oscillations that occurred during the drill.
        '''
        for i in range(total_passes):
            self.pass_ball(i, display=display)
            complete = display.update()
            if not complete:
                if verbose:
                    self.print_oscillations(i)
                break
            
        display.close()
            
    def run_hidden(self, total_passes: int, verbose: bool):
        '''Runs the simulation without the pygame display.

        Args:
            total_passes (int): The number of passes the drill is run for.
            verbose (bool): Whether to print information on oscillations that occurred during the drill.
        '''
        
        for i in range(total_passes):
            self.pass_ball(i, display=None)
        
        if verbose:
            self.print_oscillations(total_passes)
        
    def _init_lines_default(self) -> tuple[list[Player], set[Player]]:
        '''Instantiate the players and distribute them into lines from left to right.
        
        Returns:
            tuple[list[Player], set[Player]]: A list of lines with players and a set of all players.
        '''        
        lines = [[] for _ in range(self.num_lines)]
        players = set()
        pid = 0
        num_rows = self.num_players // self.num_lines
        if self.num_players % self.num_lines != 0:
            num_rows += 1
        
        for _ in range(num_rows):
            for col in range(self.num_lines):
                # check that we don't add more players than the specified number
                if (pid >= self.num_players):
                    break
                
                # initialize player
                p = Player(player_id=pid, curr_line=col)
                
                # add player to the Pygame sprite group and the lines list
                lines[col].append(p)
                players.add(p)
                pid += 1
                
        lines[self.starting_line][0].has_ball = True
        return lines, players
    
    def _init_lines_from_config(
        self, 
        line_config: dict[int, int]
    ) -> tuple[int, int, list[Player], set[Player]]:
        '''Initialize the players and distribute them 
        into lines based on the line configuration.

        Args:
            line_config (dict[int, int]): Line configuration where the key is 
            the line id and the value is the number of players in that line.

        Returns:
            tuple[int, int, list[Player], set[Player]]: The number of lines, 
            the number of players, a list of lines with players, and a set of all players.
        '''
        lines = []
        players = set()
        
        # get and check the keys representing the line ids
        keys = list(line_config.keys())
        keys.sort()
        assert all(keys[i] + 1 == keys[i + 1] for i in range(len(keys) - 1) for _ in [keys]), "Line ids must be consecutive."
        
        pid = 0
        for k in keys:
            line = [] 
            for _ in range(line_config[k]):
                p = Player(player_id=pid, curr_line=k)
                line.append(p)
                players.add(p)
                pid += 1
            lines.append(line)
            
        lines[self.starting_line][0].has_ball = True
                
        return len(keys), pid, lines, players
        
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
            
    def pass_ball(self, pass_count: int, display: Display | None):
        '''Pass the ball to the next line.

        Args:
            pass_count (int): The current number of passes that have been made.
            display (Display): The display object which shows the drill. None will result in no display.
        '''
        if self.is_last_line():
            self.flip_direction()

        next_line = self.line_with_ball - 1 if self.direction == 'left' else self.line_with_ball + 1
        if display:
            display.pass_ball(self.line_with_ball, next_line)
        self._move_player_to_next_line(self.line_with_ball, next_line, pass_count)
            
    def _move_player_to_next_line(self, curr_line: int, next_line: int, curr_pass_count: int):
        '''Move the first player in the current line to the end of the next line 
        based on the direction of the drill.

        Args:
            curr_line (int): The index of the current line.
            next_line (int): The index of the next line.
            curr_pass_count (int): The current number of passes that have been made.
        '''
        assert self.lines[next_line], f"Line {next_line + 1} is empty! Player in line {curr_line + 1} is passing to no one!"
        assert self.lines[curr_line], f"Line {curr_line + 1} is empty! Player in line {next_line + 1} is recieving from no one!"
        assert next_line != curr_line, "Player cannot pass to their current line!"
        
        player = self.lines[curr_line][0]
        
        # move the player tp end of the next line
        player.has_ball = False
        self.lines[curr_line].pop(0)
        self.lines[next_line].append(player)
        self.lines[next_line][0].has_ball = True
        self.line_with_ball = next_line
                        
        # check if an oscillation has occurred
        if (not (curr_line == 0 or curr_line == self.num_lines - 1) and
            player.previous_line == next_line):
            if player.oscillation_count == 0:
                player.pass_count_of_first_oscillation = curr_pass_count

            self.has_oscillators = True
            player.oscillation_count += 1
            
        # update current and previous line of the moving player
        player.previous_line = player.curr_line
        player.curr_line = next_line
        
    def print_oscillations(self, total_passes: int = 10):
        '''Print information on oscillations that occurred during the drill.

        Args:
            total_passes (int, optional): The total number of passes the drill was run. Defaults to 10.
        '''
        utils.printCyan(f"Total passes: {total_passes}")
        
        sorted_players = sorted(self.players, key=lambda x: x.id)
        for player in sorted_players:
            if player.oscillation_count > 0:
                percentage = player.oscillation_count / total_passes * 100
                percentage_str = f'{percentage:.1f}'
                s = f"Player {player.id:>3} oscillated {player.oscillation_count:>4} times ({percentage_str:>5}% of the drill ). Their first oscillation was on pass {player.pass_count_of_first_oscillation:>3}."
                
                utils.printRed(s) if percentage >= 2 else utils.printGreen(s)
            else:
                utils.printGreen(f"Player {player.id} did not oscillate.")
                
    def verify_line_config(self, line_config: dict[int, int] | None):
        '''Verify that the line configuration is valid. The line id must be an integer
        greater than or equal to 0 and the number of players in a line must be greater than 0.
        The key 'start_line' is also allowed. 

        Args:
            line_config (dict[int, int] | None): The line configuration to verify.

        Raises:
            KeyError: If an invalid key is found in the line configuration.
        '''
        if not line_config:
            return
        
        for key, value in line_config.items():
            assert isinstance(key, int), "Line id must be an integer."
            assert isinstance(value, int), "Number of players in a line must be an integer."
            assert key >= 0, "Invalid key in line configuration. Must be a non-negative integer or 'start_line'."
            assert value > 0, "Number of players in a line must be greater than 0."
            
    def get_player(self, player_id: int) -> Player:
        '''Get the player with the given id.

        Args:
            player_id (int): The id of the player to get.

        Returns:
            Player: The player with the given id.
        '''
        assert player_id in range(self.num_players), "Invalid player id."
        
        for player in self.players:
            if player.id == player_id:
                return player
    
    def will_oscillate(
        self, 
        player_id: int, 
        num_passes: int = math.inf
    ) -> tuple[bool, int, tuple[int, int]]:
        '''Returns data on whether a player will oscilalte over 
        num_passes passes. The data includes a boolean indicating
        if the player will oscillate, the pass on which the player 
        oscillates, and the two lines that the player oscillates between.

        Args:
            player_id (int): The id of the player to check.
            num_passes (int, optional): The number of passes to check. Defaults to math.inf.

        Returns:
            tuple[bool, int, tuple[int, int]]: Data on whether the player will oscillate over num_passes passes.
            If the player will not oscillate, returns False, -1, (-1, -1).
        '''
        assert player_id in range(self.num_players), "Invalid player id."
        assert num_passes > 0, "Number of passes must be greater than 0."
        
        oscillating_pass = -1
        oscillating_lines = (-1, -1)
        will_oscillate = False
        
        # -- Check against Lemma 2 --
        
        # if intermediate lines are all even, will_oscillate is False. Otherwise, True.
        for l in self.lines[1:-1]:
            if len(l) % 2 == 1:
                will_oscillate = True
                break
        
        # if the starting line is even, will_oscillate is True. Otherwise, 
        # depends on intermediate lines.
        will_oscillate = len(self.lines[self.starting_line]) % 2 == 0 or will_oscillate
        
        # return early if will_oscillate is False --> we know that players will 
        # never oscillate over infinite passes by Lemma 2
        if not will_oscillate:
            return will_oscillate, oscillating_pass, oscillating_lines
        
        # -- Check other conditions -- TODO: find what those are T-T
        player = self.get_player(player_id)
        start_line = player.curr_line
        
        return will_oscillate, 