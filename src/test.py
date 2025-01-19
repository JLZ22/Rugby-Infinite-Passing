import argparse
import utils
import yaml

from drill import Drill
from display import Display
from pygame.colordict import THECOLORS

num_players = 30
osc = 1000
d = Drill(num_players=num_players)
disp = Display(
    d.starting_line,
    d.lines,
    1,
    (800,800),
    frame_rate=60,
    debug=False,
    step=False,
    obj_tints={},
    bg_color=THECOLORS['azure4'],
)

parser = argparse.ArgumentParser(description='Run a drill simulation.')
parser.add_argument('-a', action='store_true', dest='a', default=False)
parser.add_argument('-c', help="Pass a configuration file to run a drill with.", dest='c', default=None)

args = parser.parse_args()
a = args.a
if args.c:
    with open(args.c, 'r') as f:
        lines_dict = yaml.safe_load(f)
        if lines_dict is not None:
            assert isinstance(lines_dict, dict), "Line config file must be a dictionary."
            if "start_line" in lines_dict:
                d.starting_line = lines_dict["start_line"]
            if 'start_direction' in lines_dict:
                d.direction = lines_dict['start_direction']
            lines_dict.pop("start_line", None)
            lines_dict.pop("start_direction", None)
if a:
    utils.print_ids(d.lines)
    projected = []
    for i in range(num_players):
        projected.append((i, d.will_oscillate(i)[1]))
    d.run_hidden(osc, False)
    real = []
    sorted_players = sorted(d.players, key=lambda x: x.id)
    for p in sorted_players:
        real.append((p.id, p.pass_count_of_first_oscillation))
        
    for p, r in zip(projected, real):
        if p[1] == r[1]:
            utils.printGreen(f'Player {p[0]}: Projected {p[1]}, Real {r[1]}')
        else:
            utils.printRed(f'Player {p[0]}: Projected {p[1]}, Real {r[1]}')
else:
    print(d.will_oscillate(5))
    d.run_visible(osc, disp, True)