from functools import partial
from multiprocessing import Pool
import turtle
from tqdm import tqdm

SYSTEM_RULES = {}  # generator system rules for l-system

def parallel_derivation(axiom, steps, n_workers=1, system_rules=SYSTEM_RULES):
    derived = [axiom]  # seed
    p = Pool(n_workers)
    for _ in tqdm(range(steps)):
        next_seq = derived[-1]
        next_axiom = p.map(partial(rule, system_rules=system_rules), next_seq)
        derived.append(''.join(next_axiom))
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

def draw_l_system(turtle, SYSTEM_RULES, seg_length, angle):
    stack = []
    for command in SYSTEM_RULES:
        turtle.pd()
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
    return r_turtle