from functools import partial
from multiprocessing import Pool
import turtle
from tqdm import tqdm

SYSTEM_RULES = {}  # generator system rules for l-system

def parallel_derivation(axiom, steps, n_workers=1, system_rules=SYSTEM_RULES):
    derived = axiom  # seed
    p = Pool(n_workers)
    for _ in tqdm(range(steps)):
        next_axiom = p.map(partial(rule, system_rules=system_rules), derived)
        derived = ''.join(next_axiom)
    return derived

def derivation(axiom, steps):
    derived = [axiom]  # seed
    for _ in range(steps):
        next_seq = derived[-1]
        next_axiom = [rule(char) for char in next_seq]
        derived.append(''.join(next_axiom))
    return derived


def rule(sequence, system_rules):
    if sequence in system_rules:
        return system_rules[sequence]
    return sequence

def pick_color(palette):
    for color in palette:
        yield color

def draw_l_system(turtle, SYSTEM_RULES, seg_length, angle):
    stack = []
    palette = ["9D6079","A06079","A35F78","A75F78","AA5F78","AD5E77","B05E77","B35E77","B75E77","BA5D76","BD5D76","C05D76","C35C75","C75C75","CA5C75","CD5B74","D05B74","D45B74","D75A73","DA5A73","DD5A73","E05972","E45972","E75972","EA5972","ED5871","F05871","F45871","F75770","FA5770"]

    for ix, command in enumerate(SYSTEM_RULES):
        turtle.pd()
        if ix % len(palette) == 0:
            turtle.pencolor(f"#{next(pick_color(palette))}")
        if command in ["F", "G", "R", "L"]:
            turtle.forward(seg_length)
        elif command == "f":
            turtle.pu()  # pen up - not drawing
            turtle.forward(seg_length)
        elif command == "+":
            turtle.right(angle)
        elif command == "-":
            turtle.left(angle)
        elif command == "[":
            stack.append((turtle.position(), turtle.heading()))
        elif command == "]":
            turtle.pu()  # pen up - not drawing
            position, heading = stack.pop()
            turtle.goto(position)
            turtle.setheading(heading)


def set_turtle(alpha_zero):
    r_turtle = turtle.Turtle()  # recursive turtle
    r_turtle.screen.title("L-System Derivation")
    r_turtle.speed(0)  # adjust as needed (0 = fastest)
    r_turtle.setheading(alpha_zero)  # initial heading
    #r_turtle.color("#fa5770")
    return r_turtle