import random


_SYNONYMS = {
    "Place": ["Put", "Set", "Move", "Position"],
    "Stack": ["Place", "Put", "Set"],
    "Pick up": ["Grab", "Take", "Lift"],
    "on top of": ["onto", "on", "above"],
    "then": ["after that", "next", "and then", "subsequently"],
    "First": ["To start", "Begin by", "Initially"],
    "block": ["cube", "piece", "brick"],
}


def augment(examples: list[dict], rng: random.Random) -> list[dict]:
    augmented = []
    for ex in examples:
        user_msg = ex["messages"][1]["content"]
        instruction_line = user_msg.split("\n")[0].replace("Instruction: ", "")
        new_instruction = instruction_line
        for original, replacements in _SYNONYMS.items():
            if original in new_instruction and rng.random() > 0.5:
                new_instruction = new_instruction.replace(original, rng.choice(replacements), 1)

        if new_instruction != instruction_line:
            new_user = user_msg.replace(instruction_line, new_instruction)
            new_ex = {
                "messages": [
                    ex["messages"][0],
                    {"role": "user", "content": new_user},
                    ex["messages"][2],
                ]
            }
            augmented.append(new_ex)
    return augmented