from functools import partial
from multiprocessing import Pool
import turtle
from colour import Color
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

def sequenced_gradient(colors, size=60):
    colors_per_pair = int(size / len(colors)) + 1
    sequenced_pallete = []
    for ix in range(1, len(colors)):
        sequenced_pallete += list(Color(colors[ix - 1]).range_to(Color(colors[ix]), colors_per_pair))
    return sequenced_pallete

def draw_l_system(turtle, SYSTEM_RULES, seg_length, angle, palette="blue_pink_grad_var"):
    stack = []
    palettes = {
        "lavender_pink_grad": list(Color("#9D6079").range_to(Color("#FA5770"), 60)),
        "blue_pink_grad": list(Color("#7eb8da").range_to(Color("#ffa5d8"), 60)),
        "blue_pink_grad_var": sequenced_gradient(["#7eb8da", "#92ddea", "#be9ddf", "#ffa5d8"], 60)
    }
    palette_iter = palettes[palette]

    color_change_ix = len(SYSTEM_RULES) // len(palettes[palette])

    for ix, command in enumerate(SYSTEM_RULES):
        turtle.pd()
        
        if (ix % color_change_ix == 0) and (any(palette_iter)):
            next_color = palette_iter.pop()
            turtle.pencolor(f"{next_color}")      
        
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