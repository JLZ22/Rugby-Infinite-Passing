from Drill import Drill
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Run a simulation of infinite passing.')
    
    parser.add_argument("--speed", help="Speed of the drill", default=10)
    parser.add_argument("--players", help="Number of players", default=10)
    parser.add_argument("--lines", help="Number of lines", default=4)
    parser.add_argument("--start-line", help="Starting line", default=0)
    parser.add_argument("--passes", help="Number of passes", default=10)
    
    parser.add_argument("--no-display", help="Do not display the drill", action="store_false", dest="display")
    parser.add_argument("--display", help="Display the drill", action="store_true", dest="display")
    
    parser.add_argument("--silent", help="Do not print the drill", action="store_false", dest="verbose")
    parser.add_argument("--verbose", help="Print the drill", action="store_true", dest="verbose")
    
    # examples 
    parser.add_argument("--example1", help="Run example 1", action="store_true")
    parser.add_argument("--example2", help="Run example 2", action="store_true")

    args = parser.parse_args()
    
    if args.example1:
        args.speed = 10
        args.players = 5
        args.display = True
        args.lines = 4
        args.start_line = 0
        args.passes = 5
        args.verbose = True
    elif args.example2:
        args.speed = 10
        args.players = 7
        args.display = True
        args.lines = 4
        args.start_line = 0
        args.passes = 8
        args.verbose = True
        
    return args
                
if __name__ == "__main__":
    args = parse_args()
    
    drill = Drill(
        num_lines=args.lines,
        num_players=args.players, 
        starting_line=args.start_line
        )
    drill.run(
        speed=args.speed, 
        total_passes=args.passes, 
        display=args.display,
        verbose=args.verbose
    )