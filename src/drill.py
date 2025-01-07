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
    ):
        '''Constructs a drill.

        Args:
            num_lines (int, optional): Number of lines in the drill. Defaults to 4.
            num_players (int, optional): Total number of players in the drill. Defaults to 15.
            starting_line (int, optional): The index of the line that starts with the ball. Defaults to 0.
        '''
        assert num_lines < num_players + 1, "Number of lines must be less than number of players + 1"
        assert num_lines > 1, "Number of lines must be greater than 1"
        self.num_lines = num_lines
        self.num_players = num_players
        self.direction = 'right'
        self.starting_line = self.line_with_ball = starting_line
        self.has_oscillators = False # Flag to check if any player has oscillated
        self.moving_players = set() # List of players whose paths have been changed
        self.lines, self.players = self._init_lines()
        
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
        
    def _init_lines(self) -> tuple[list[Player], set[Player]]:
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