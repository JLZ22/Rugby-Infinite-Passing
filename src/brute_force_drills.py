from Drill import Drill
import utils
import argparse
import yaml

'''
Runs every combination of lines and players up to max_lines and max_players_coefficient * max_lines
and runs num_iterations for each combination. Prints out results if there are no oscillations or 
if there are no successful runs for a given number of lines.
'''
def run_drills(max_lines: int, max_players_coefficient: int, num_iterations: int) -> str:
    save = ""
    num_instances = [0] * (max_lines + 1)
    num_instances[0] = -1
    num_instances[1] = -1

    for num_lines in range(2, max_lines + 1):
        contains_success = False
        player_range = range(num_lines + 1, num_lines * max_players_coefficient + 1)
        txt = f'{num_lines} lines | {num_iterations:,} iterations' + '-' * 25 + '\n'
        save += txt
        print(txt, end="")
        for num_players in player_range:
            drill = Drill(num_lines, num_players)
            r = drill.run(num_iterations, verbose=False)
            del drill 

            if not r:
                contains_success = True
                txt = f"No oscillations for {num_players:>3} players.\n"
                num_instances[num_lines] += 1
                save += txt
                utils.printGreen(txt, end="")
        
        if not contains_success:
            txt = f"No successful runs for {num_lines:>3} lines over following range of players: {player_range}.\n"
            save += utils.formatRed(f"No successful runs for {num_lines:>3} lines over following range of players: {player_range}.\n")
            utils.printRed(txt, end="")

    save += "\n\n" + "-" * 25 + "\n\n"
    instance_report = ""
    curr_val = num_instances[2]
    range_report = {curr_val: (2, 2)}
    for i, count in enumerate(num_instances):
        if count == -1:
            continue
        if count == curr_val:
            range_report[curr_val] = (range_report[curr_val][0], i)
        else:
            curr_val = count
            range_report[curr_val] = (i, i)

    for key, val in range_report.items():
        if val[0] == val[1]:
            instance_report += f"Line {val[0]}: {key} unique player counts result in no oscillations\n"
        else:
            instance_report += f"Lines {val[0]}-{val[1]}: {key} unique player counts result in no oscillations\n"
    print(instance_report)
    save += instance_report
    return save


'''
Performs a brute force search for the number of lines and players that will not have oscillations.

Example of a valid config file:

max lines: 100
players coefficient: 10
iterations: 1000
'''
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run a drill.')
    parser.add_argument("--config", help="Path to yaml config file.", default=None)

    args = parser.parse_args()

    max_lines = 100
    max_players_coefficient = 10
    num_iterations = 1000


    if args.config:
        with open(args.config, "r") as f:
            config = yaml.safe_load(f)
            if "max lines" in config and config["max lines"] > 1:
                max_lines = config["max lines"]

            if "players coefficient" in config and config["players coefficient"] > 1:
                max_players_coefficient = config["players coefficient"]
            
            if "iterations" in config and config["iterations"] > 1:
                num_iterations = config["iterations"]

    save = run_drills(max_lines, max_players_coefficient, num_iterations)

    from pathlib import Path

    with open(Path(f"results/Lines-{max_lines}_PlayersCoefficient-{max_players_coefficient}_Iterations-{num_iterations}.txt"), "w") as f:
        f.write(save)