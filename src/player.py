class Player():
    '''A player in the drill. Functions as a storage class for player data.
    '''
    def __init__(self, player_id: int, curr_line: int):
        '''Constructor for Player class.

        Args:
            player_id (int): Unique player id.
            curr_line (int): Line that player is currently in. 
        '''
        self.id = player_id
        self.has_ball = False
        self.previous_line = -1
        self.oscillation_count = 0
        self.iteration_of_first_oscillation = -1
        self.curr_line = curr_line