SINGLE_STEP_TEMPLATES = [
    "Place the {a} block on the {b} block.",
    "Stack {a} on top of {b}.",
    "Put the {a} block onto the {b} block.",
    "Move {a} on {b}.",
    "Take the {a} block and place it on {b}.",
    "Pick up the {a} block and stack it on the {b} block.",
    "Set the {a} block on top of the {b} one.",
    "Grab {a} and put it on {b}.",
]

TWO_STEP_TEMPLATES = [
    "Stack the {a} block on the {b} block, then place the {c} block on top.",
    "First put {a} on {b}, then stack {c} on {a}.",
    "Place {a} on top of {b}. After that, put {c} on top of {a}.",
    "Build a tower: {b} on the bottom, {a} in the middle, {c} on top.",
    "Stack {a} onto {b}, and then {c} onto {a}.",
    "Put {a} on {b}. Next, put {c} on {a}.",
    "First stack {a} on {b}, then add {c} on top of the stack.",
    "Move {a} onto {b} and then move {c} onto {a}.",
]

THREE_STEP_TEMPLATES = [
    "Stack {a} on {b}, then {c} on {a}, then {d} on {c}.",
    "Build a tower from bottom to top: {b}, {a}, {c}, {d}.",
    "Place {a} on {b}. Then put {c} on {a}. Finally place {d} on {c}.",
    "First {a} on {b}, next {c} on {a}, last {d} on {c}.",
]

ERROR_TEMPLATES = [
    "Place the {a} block on the {a} block.",
    "Stack {a} on itself.",
]