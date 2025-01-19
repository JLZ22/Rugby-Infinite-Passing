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
        count = 0
        for i in range(total_passes):
            count = i
            self.pass_ball(i, display=display)
            complete = display.update()
            if not complete:
                break
        if verbose:
            self.print_oscillations(count)
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
            
    def get_line(self, player: int | Player) -> int:
        '''Gets the index of the line that the player is in.

        Args:
            player (int | Player): The player to get the line of.

        Raises:
            ValueError: If the player is not found in any line.

        Returns:
            int: The index of the line that the player is in.
        '''
        if player is int:
            assert player in range(self.num_players), "Invalid player id."
            player = self.get_player(player)
            
        for i in range(self.num_lines):
            if player in self.lines[i]:
                return i
            
        raise ValueError(f"Player not found in any line: {player}")

    def is_perfect(self) -> bool:
        '''Finds if the drill is perfect. A drill is perfect if all intermediate
        lines have an even number of players except for the starting line which
        must have an odd number of players unless the starting line is 
        one of the end lines.

        Returns:
            bool: True if the drill is perfect, False otherwise.
        '''
        # if starting line is an intermediate line and has an even number of players
        # drill is not perfect
        if self.starting_line in range(1, self.num_lines - 1) and len(self.lines[self.starting_line]) % 2 == 0:
            return False
        
        # if all intermediate lines have an even number of players, drill is perfect
        for i in range(1, self.num_lines - 1):
            if i != self.starting_line and len(self.lines[i]) % 2 == 1:
                return False
            
        return True
    
    def get_player_rank(self, player: int | Player) -> int:
        '''Get the rank of the player in their line.

        Args:
            player (int | Player): The id of the player or the player object.

        Raises: 
            ValueError: If the player is not found in any line.

        Returns:
            int: The rank of the player in their line.
        '''
        if player is int:
            assert player_id in range(self.num_players), "Invalid player id."
            player = self.get_player(player_id)
            
        line = self.lines[player.curr_line]
        for i, p in enumerate(line):
            if p == player:
                return i
            
        raise ValueError(f"Player not found in any line: {player}")
    
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
        
        # --------- Check against a perfect drill ---------
        # this is for early stopping
        will_oscillate = not self.is_perfect()
        if not will_oscillate:
            return will_oscillate, oscillating_pass, oscillating_lines
        
        # --------- Implement main algorithm ---------
        
        player = self.get_player(player_id)
        player_rank = self.get_player_rank(player)
        curr_line = player.curr_line
        ball_dir = self._get_first_pass_direction(curr_line)
        player_direction = ball_dir if player_rank % 2 == 0 else not ball_dir
        target_line = self._get_first_odd_line(player_direction, curr_line)
        if target_line == -1:
            return will_oscillate, oscillating_pass, oscillating_lines
        
        def get_next_line():
            nonlocal player_direction
            nonlocal ball_dir
            # change directions if needed
            if curr_line == 0:
                player_direction = False
            elif curr_line == self.num_lines - 1:
                player_direction = True
                
            ball_dir = player_direction
                
            # get the next line based on the direction
            if player_direction:
                return curr_line - 1
            return curr_line + 1
        
        # ------- Find the number of passes until the player oscillates -------
        
        # get number of passes from starting line to line with player
        passes = self._get_passes_until_line(curr_line, self.starting_line, ball_dir)
        
        # get number passes until the player is first in their line 
        passes_til_first = self._get_passes_until_player_first(
            player_rank,
            ball_dir,
            curr_line
        )
        passes += passes_til_first        
        # pass the ball to the next line and update the current line
        passes += 1
        curr_line = get_next_line()        
        
        # while the player is not in the target line, calculate the number of passes
        # until the player is first in their line and then pass the ball to the next line
        while curr_line != target_line:
            passes_til_first = self._get_passes_until_player_first(
                len(self.lines[curr_line]) if curr_line != self.starting_line else len(self.lines[curr_line]) - 1, # we know that starting line has one less player than initial count by lemma 2
                ball_dir, 
                curr_line
            )
            passes += passes_til_first + 1
            curr_line = get_next_line()
            
        # player is now at the end of the target line
        # calculate the number of passes until the player is first in their line
        passes_til_first = self._get_passes_until_player_first(
            len(self.lines[target_line]),
            ball_dir,
            target_line
        )
        passes += passes_til_first
                
        # this is the pass on which the player will oscillate
        passes += 1
        
        if passes <= num_passes:
            will_oscillate = True
            oscillating_pass = passes
            line_1 = target_line
            line_2 = target_line - 1 if player_direction else target_line + 1
            oscillating_lines = (line_1, line_2)
        
        return will_oscillate, oscillating_pass, oscillating_lines
        
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
                player.pass_count_of_first_oscillation = curr_pass_count + 1

            self.has_oscillators = True
            player.oscillation_count += 1
            
        # update current and previous line of the moving player
        player.previous_line = player.curr_line
        player.curr_line = next_line
    
    def _get_first_odd_line(self, left: bool, curr_line: int) -> int:
        '''Gets the index  of the closest odd line ot the 
        curr_line in the specified direction. If there is no 
        odd line in the specified direction, it will return 
        the closest odd line in the other direction. This will 
        only count the curr_line if there is no odd line in the 
        specified direction.

        Args:
            left (bool): Whether the direction is left or right.
            curr_line (int): The line to start from.

        Returns:
            int: The index of the closest odd line. Will return -1 if 
            no odd line is found excluding the curr_line and the end 
            lines.
        '''
        def search_left():
            # exclude the first line because its parity doesn't matter
            for i in range(1, curr_line):
                if self.check_line(i):
                    return i
            return -1
        def search_right():
            # exclude the last line because its parity doesn't matter
            for i in range(curr_line + 1, self.num_lines - 1):
                if self.check_line(i):
                    return i
            return -1
                
        first = -1
        if left:
            first = search_left()
            if self.check_line(curr_line):
                return curr_line
            if first == -1:
                first = search_right()
        else:
            first = search_right()
            if self.check_line(curr_line):
                return curr_line
            if first == -1:
                first = search_left()
                
        return first
    
    def check_line(self, line_num: int) -> bool:
        '''Check if the line will cause an oscillation.

        Args:
            line_num (int): The index of the line to check.

        Returns:
            bool: True if the line will cause an oscillation, False otherwise.
        '''
        if line_num in range(1, self.num_lines - 1):
            if line_num == self.starting_line and len(self.lines[line_num]) % 2 == 0:
                return True
            if len(self.lines[line_num]) % 2 == 1:
                return True
        return False
    
    def _get_passes_until_player_first(
        self, 
        player_rank: int,
        left: bool, 
        line_num: int
    ) -> int:
        '''Finds the number of passes before the player at player_rank of 
        line_num is first with the ball. The direction of the search is

        Args:
            player_rank (int): The rank of the player in the line (0-indexed).
            left (bool): The direction of the first pass.
            line_num (int): The line the player is in. (0-indexed)

        Returns:
            int: The number of passes until the player is first with the ball.
        '''
        assert line_num in range(self.num_lines), "Invalid line number."
        
        lines_left = line_num
        lines_right = self.num_lines - line_num - 1
        extra = player_rank % 2 # extra pass if there is an odd number of players ahead of the player at player_rank
        
        if line_num == 0:
            return player_rank * lines_right * 2
        if line_num == self.num_lines - 1:
            return player_rank * lines_left * 2
        
        # half the players ahead go left and half go right
        # in the event that there is an odd number of players ahead of the player,
        # the extra player will go in the starting directionk
        if left:
            return (player_rank // 2 * lines_left * 2 + extra * lines_left * 2) + (player_rank // 2 * lines_right * 2)
        return (player_rank // 2 * lines_right * 2 + extra * lines_right * 2) + (player_rank // 2 * lines_left * 2)
    
    def _get_first_pass_direction(
        self,
        line_num: int
    ) -> bool:
        '''Finds the direction of the first pass of 
        the line with the given index.

        Args:
            line_num (int): The index of the line to check.

        Returns:
            bool: True if the first pass is left, False otherwise.
        '''
        if line_num == self.starting_line:
            return self.direction == 'left'
        return line_num < self.starting_line
    
    def _get_passes_until_line(
        self,
        target_line: int,
        start_line: int, 
        left: bool
    ) -> int:
        '''Get the number of passes to get from the 
        start line to the target line given the starting 
        direction.

        Args:
            target_line (int): The index of the target line.
            start_line (int): The index of the start line.
            left (bool): The starting direction.

        Returns:
            int: The number of passes to get from the start line to the target line.
        '''
        if target_line == start_line:
            return 0
        
        if left:
            if target_line < start_line:
                return start_line - target_line
            return target_line + start_line
        
        # direction is right
        if target_line > start_line:
            return target_line - start_line
        return self.num_lines - start_line + self.num_lines - target_line