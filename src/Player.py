from SimulationObject import SimulationObject

class Player(SimulationObject):
    '''A player in the drill. 

    Args:
        SimulationObject (SimulationObject): A parent class for all objects in the simulation.
    '''
    def __init__(self, x: int, y: int, player_id: int, curr_line: int, speed: int = 5):
        '''Constructor for Player class.

        Args:
            x (int): Starting x position.
            y (int): Starting y position.
            player_id (int): Unique player id.
            curr_line (int): Line that player is currently in. 
            speed (int, optional): The speed that the player moves. Defaults to 5.
        '''
        super().__init__(img_path='../assets/player.png', x=x, y=y, speed=speed)
        self.id = player_id
        self.has_ball = False
        self.previous_line = -1
        self.oscillation_count = 0
        self.iteration_of_first_oscillation = -1
        self.curr_line = curr_line