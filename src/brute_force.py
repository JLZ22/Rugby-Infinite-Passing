from drill import Drill
import utils
import argparse

'''
Runs every combination of lines and players up to max_lines and max_players_coefficient * max_lines
and runs num_passes for each combination. Prints out results if there are no oscillations or 
if there are no successful runs for a given number of lines.
'''
def run_drills(max_lines: int, max_players_coefficient: int, num_passes: int) -> str:
    save = ""
    num_instances = [0] * (max_lines + 1)
    num_instances[0] = -1
    num_instances[1] = -1

    for num_lines in range(2, max_lines + 1):
        contains_success = False
        player_range = range(num_lines + 1, num_lines * max_players_coefficient + 1)
        txt = f'{num_lines} lines | {num_passes:,} iterations' + '-' * 25 + '\n'
        save += txt
        print(txt, end="")
        for num_players in player_range:
            drill = Drill(num_lines, num_players)
            r = drill.run(num_passes, verbose=False, display=False)
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

def parse_args():
    parser = argparse.ArgumentParser(description="Find the line + player combinations that do not have oscillations over a given number of passes.")
    parser.add_argument("--max-lines", help="Maximum number of lines to test.", default=100, type=int)
    parser.add_argument("--coefficient", help="This number is multiplied by the number of lines to determine the maximum number of players for a given number of lines.", default=10, type=int)
    parser.add_argument("--passes", help="Number of passes to run for each combination of lines and players.", default=1000, type=int)

    return parser.parse_args()

'''
Performs a brute force search for the number of lines and players that will not have oscillations.
'''
if __name__ == "__main__":
    args = parse_args()
    
    m,c,p = args.max_lines, args.coefficient, args.passes

    save = run_drills(m, c, p)

    from pathlib import Path

    with open(Path(f"results/Lines-{m}_PlayersCoefficient-{c}_Passes-{p}.txt"), "w") as f:
        f.write(save)