import argparse
import yaml

from display import Display
from drill import Drill
from pygame.colordict import THECOLORS

WIN_SIZE = (800, 600)
BG_COLOR = THECOLORS['azure4']
FRAME_RATE = 60

def parse_args() -> argparse.Namespace:
    '''Parse command line arguments. Setting the example flag will override 
    all other arguments except speed and colors. Example 1 takes precedence over example 2.

    Returns:
        Namespace: The parsed arguments. 
    '''
    parser = argparse.ArgumentParser(description='Run a simulation of infinite passing.')
    
    # --- Simulation parameters ---
    parser.add_argument("--players", help="Number of players", default=10, type=int)
    parser.add_argument("--lines", help="Number of lines", default=4, type=int)
    parser.add_argument("--start-line", help="Starting line", default=0, type=int)
    parser.add_argument("--passes", help="Number of passes", default=10, type=int)
    parser.add_argument("--direction", help="Starting direction of the drill", default="right", choices=["right", "left"])
    
    parser.add_argument("--speed", help="Speed of the display", default=300, type=int)
    parser.add_argument("--silent", help="Do not print the oscillation data.", action="store_false", dest="verbose", default=True)
    parser.add_argument("--hidden", help="Do not display the drill", action="store_false", dest="display", default=True)
    parser.add_argument("--step", help="Step through the simulation using space bar.", action="store_true", default=False)
    parser.add_argument("--debug", help="Display player ids insteda of images.", action="store_true", default=False)
    
    # config files
    parser.add_argument("--colors", help="Yaml file with display object colors based on id. Ball id is -1. Background is -2.", default=None)
    '''
    # colors.yaml
    # You can use the color names from the pygame.colordict.THECOLORS dictionary, RGB, or RGBA.
    # RGB/RGBA values must be between 0 and 255. They must also be passed in as a list as shown below.
    -1: # the ball
        - 255
        - 0
        - 0
    0: 
        - 0
        - 255
        - 0
        - 100
    1: blueviolet
    '''
    
    parser.add_argument("--line-config", help="Yaml file with line configuration. This will override --lines and --players.", default=None)
    '''
    # line_config.yaml
    # key is the line id and the value is the number of players in that line.
    0: 5
    1: 5
    2: 1 
    3: 3
    
    # if you want to override the --start-line flag, add a key 'start_line'
    start_line: 0
    # 
    start_direction: right
    '''
    
    # examples 
    parser.add_argument("--example1", help="Run example 1", action="store_true")
    parser.add_argument("--example2", help="Run example 2", action="store_true")

    # --- Parse arguments ---
    args = parser.parse_args()
    args.obj_tints = {}
    args.lines_dict = None
    args.bg_color = BG_COLOR
    
    # --- Load config files ---
    if args.colors:
        with open(args.colors, "r") as f:
            cols = yaml.safe_load(f)
            if cols is not None:
                args.obj_tints = cols
                assert isinstance(args.obj_tints, dict), f"Colors file must be a dictionary."
                if -2 in args.obj_tints:
                    args.bg_color = args.obj_tints[-2]
    if args.line_config:
        with open(args.line_config, "r") as f:
            args.lines_dict = yaml.safe_load(f)
            if args.lines_dict is not None:
                assert isinstance(args.lines_dict, dict), "Line config file must be a dictionary."
                if "start_line" in args.lines_dict:
                    args.start_line = args.lines_dict["start_line"]
                if 'start_direction' in args.lines_dict:
                    args.direction = args.lines_dict['start_direction']
                args.lines_dict.pop("start_line", None)
                args.lines_dict.pop("start_direction", None)
    
    # --- Examples ---
    if args.example1:
        args.players = 5
        args.display = True
        args.lines = 4
        args.start_line = 0
        args.passes = 5
        args.verbose = True
        args.obj_tints = {1: THECOLORS["red"]}
        args.step = False
        args.lines_dict = None
    elif args.example2:
        args.players = 7
        args.display = True
        args.lines = 4
        args.start_line = 0
        args.passes = 9
        args.verbose = True
        args.obj_tints = {1: THECOLORS["green"]}
        args.step = False
        args.lines_dict = None
        
    return args
                
if __name__ == "__main__":
    '''For help on command line arguments, run with the -h flag.
    '''
    args = parse_args()
    
    drill = Drill(
        num_lines=args.lines,
        num_players=args.players, 
        starting_line=args.start_line,
        direction=args.direction,
        line_config=args.lines_dict,
    )
    
    if args.display:
        display = Display(
            start_line=args.start_line,
            lines=drill.lines,
            speed=args.speed,
            win_size=WIN_SIZE,
            obj_tints=args.obj_tints,
            bg_color=args.bg_color,
            frame_rate=FRAME_RATE,
            step=args.step,
            debug=args.debug,
        )
        
        drill.run_visible(args.passes, display, args.verbose)
    else:
        drill.run_hidden(args.passes, args.verbose)