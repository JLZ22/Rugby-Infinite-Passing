import argparse
import utils
import yaml

from drill import Drill

def parse_args() -> argparse.Namespace:
    '''Parse command line arguments.

    Returns:
        argparse.Namespace: The parsed arguments.
    '''
    parser = argparse.ArgumentParser(description='Given a drill, number of passes, and a player id, determine if the player will oscillate over the course of the drill.')
    
    # --- Simulation parameters ---
    parser.add_argument("--players", help="Number of players", default=10, type=int)
    parser.add_argument("--lines", help="Number of lines", default=4, type=int)
    parser.add_argument("--start-line", help="Starting line", default=1, type=int)
    parser.add_argument("--passes", help="Number of passes", default=100, type=int)
    parser.add_argument("--inf", help="Set the number of passes to infinity.", action="store_true")
    parser.add_argument("--direction", help="Starting direction of the drill", default="right", choices=["right", "left"])
    parser.add_argument("--line-config", help="Yaml file with line configuration. This will override --lines and --players.", default=None)
    parser.add_argument("--player-id", help="Player id to check if they will oscillate.", default=0, type=int)
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
    
    args = parser.parse_args()
    args.line_dict = {}
    if args.line_config:
        with open(args.line_config, 'r') as f:
            lines_dict = yaml.safe_load(f)
            if lines_dict is not None:
                assert isinstance(lines_dict, dict), "Line config file must be a dictionary."
                if "start_line" in lines_dict:
                    args.start_line = lines_dict["start_line"]
                if 'start_direction' in lines_dict:
                    args.direction = lines_dict['start_direction']
                lines_dict.pop("start_line", None)
                lines_dict.pop("start_direction", None)
                args.line_dict = lines_dict
                
    if args.inf:
        args.passes = float('inf')
                
    return args

def main():
    '''
    Run a drill simulation and project if a player will oscillate.
    '''
    print('-' * 50)
    print('Drill Parameters')
    args = parse_args()
    d = Drill(
        num_players=args.players,
        num_lines=args.lines,
        starting_line=args.start_line,
        direction=args.direction,
        line_config=args.line_dict
    )
    print('    Number of Players:', d.num_players)
    print('    Number of Lines:', d.num_lines)
    print('    Starting Line:', d.starting_line)
    print('    Starting Direction:', d.direction)
    print('    Number of Passes:', args.passes)
    
    projection_result = d.will_oscillate(args.player_id, args.passes)
    if not args.inf:
        d.run_hidden(args.passes, False)
        sorted_players = sorted(d.players, key=lambda x: x.id)
        p = sorted_players[args.player_id]
        if p.pass_count_of_first_oscillation != projection_result[1]:
            utils.printRed(f'Projection deviated from simulation.');
        else:
            utils.printGreen(f'Projection accurate.');
        print(f'Simulation Result:', end=' ')
        if p.pass_count_of_first_oscillation == -1:
            print(f'Player {args.player_id} did not oscillate.')
        else:
            print(f"Player {p.id}'s first oscillation was at pass {p.pass_count_of_first_oscillation}.")
    else:
        print('Because the number of passes is set to infinity, the simulation result is not available.')
    
    print(f'Projected Result:', end='  ')
    if projection_result[1] == -1:
        print(f'Player {args.player_id} will not oscillate.')
    else:
        print(f'Player {args.player_id} will oscillate between lines {projection_result[2][0]} and {projection_result[2][1]} on pass {projection_result[1]}.')

if __name__ == "__main__":
    main()