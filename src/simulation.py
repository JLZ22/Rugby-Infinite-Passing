import argparse

from display import Display
from drill import Drill
from pygame.colordict import THECOLORS

WIN_SIZE = (800, 600)
BG_COLOR = THECOLORS['azure4']
FRAME_RATE = 60

def parse_args() -> argparse.Namespace:
    '''Parse command line arguments. Setting the example flag will override 
    all other arguments except speed. Example 1 takes precedence over example 2.

    Returns:
        Namespace: The parsed arguments. 
    '''
    parser = argparse.ArgumentParser(description='Run a simulation of infinite passing.')
    
    parser.add_argument("--players", help="Number of players", default=10, type=int)
    parser.add_argument("--lines", help="Number of lines", default=4, type=int)
    parser.add_argument("--start-line", help="Starting line", default=0, type=int)
    parser.add_argument("--passes", help="Number of passes", default=10, type=int)
    
    parser.add_argument("--speed", help="Speed of the display", default=300, type=int)
    parser.add_argument("--silent", help="Do not print the oscillation data.", action="store_false", dest="verbose", default=True)
    parser.add_argument("--hidden", help="Do not display the drill", action="store_false", dest="display", default=True)
    parser.add_argument("--step", help="Step through the simulation using space bar.", action="store_true", default=False)
    parser.add_argument("--debug", help="Display player ids insteda of images.", action="store_true", default=False)
        
    # examples 
    parser.add_argument("--example1", help="Run example 1", action="store_true")
    parser.add_argument("--example2", help="Run example 2", action="store_true")

    args = parser.parse_args()
    args.player_tints = {}
    
    if args.example1:
        args.players = 5
        args.display = True
        args.lines = 4
        args.start_line = 0
        args.passes = 5
        args.verbose = True
        args.player_tints = {1: THECOLORS["red"]}
        args.step = False
    elif args.example2:
        args.players = 7
        args.display = True
        args.lines = 4
        args.start_line = 0
        args.passes = 9
        args.verbose = True
        args.player_tints = {1: THECOLORS["green"]}
        args.step = False
        
    return args
                
if __name__ == "__main__":
    '''For help on command line arguments, run with the -h flag.
    '''
    args = parse_args()
    
    drill = Drill(
        num_lines=args.lines,
        num_players=args.players, 
        starting_line=args.start_line,
    )
    
    display = Display(
        start_line=args.start_line,
        lines=drill.lines,
        speed=args.speed,
        win_size=WIN_SIZE,
        player_tints=args.player_tints,
        ball_tint=None,
        bg_color=BG_COLOR,
        frame_rate=FRAME_RATE,
        step=args.step,
        debug=args.debug,
    )
    
    if args.display:
        drill.run_visible(args.passes, display, args.verbose)
    else:
        drill.run_hidden(args.passes, args.verbose)