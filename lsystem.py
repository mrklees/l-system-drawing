import argparse
import json
import turtle
from utils import *


def get_ruleset(path="ruleset.json"):
    with open(path) as f:
        rules = f.read()
        return json.loads(rules)


def parse_args():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-n', '--name', default="dragon_curve", type=str,
                        help='Which figure do you want to render?')
    parser.add_argument('-i', '--iter', default=None, type=int,   
                        help='How many iterations to run? Careful, more than 25 is probably too many unless you have a lot of time.')
    parser.add_argument('-w', '--workers', default=4, type=int,   
                        help='How many workers to use?')
    parser.add_argument('-s', '--step', default=None, type=float,   
                        help='How long should each step be?')
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_args()
    
    ruleset = get_ruleset()
    rules = ruleset[args.name]
    for r in rules['ruleset']:
        key, value = r.split("->")
        SYSTEM_RULES[key] = value
    
    axiom = rules['axiom']
    if args.iter is None:
        iterations = rules['iterations']
    else:
        iterations = args.iter
    if args.step is None:
        segment_length = rules['step_size']  
    else:
        segment_length = args.step
    alpha_zero = rules['initial_heading']
    angle = rules['angle_increment']

    model = parallel_derivation(
        axiom, 
        iterations, 
        n_workers=8, 
        system_rules=SYSTEM_RULES
    )

    r_turtle = set_turtle(alpha_zero)
    turtle_screen = turtle.Screen()
    turtle_screen.screensize(4500, 4500)
    turtle_screen.bgcolor("#fefdfe")
    draw_l_system(r_turtle, model, segment_length, angle)
    turtle_screen.exitonclick()
