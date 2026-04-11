import random
import itertools
from data_generation.constants import DEFAULT_COLORS
from data_generation.templates import SINGLE_STEP_TEMPLATES, TWO_STEP_TEMPLATES, THREE_STEP_TEMPLATES, ERROR_TEMPLATES
from data_generation.generation import make_plan_single, make_plan_two, make_plan_three, make_error_plan, make_random_scene
from data_generation.formatting import format_example
from data_generation.augmentation import augment


def generate_examples(
    colors: list[str] | None = None,
    target_count: int = 800,
    seed: int = 42,
) -> list[dict]:
    rng = random.Random(seed)
    colors = colors or DEFAULT_COLORS
    examples: list[dict] = []

    # Single-step examples
    for a, b in itertools.permutations(colors, 2):
        template = rng.choice(SINGLE_STEP_TEMPLATES)
        instruction = template.format(a=a, b=b)
        scene = make_random_scene(colors)
        plan = make_plan_single(a, b)
        examples.append(format_example(instruction, scene, plan))

    # Two-step examples (tower of 3)
    for a, b, c in itertools.permutations(colors, 3):
        template = rng.choice(TWO_STEP_TEMPLATES)
        instruction = template.format(a=a, b=b, c=c)
        scene = make_random_scene(colors)
        plan = make_plan_two(a, b, c)
        examples.append(format_example(instruction, scene, plan))

    # Three-step examples (need ≥4 colors)
    if len(colors) >= 4:
        for combo in itertools.permutations(colors, 4):
            a, b, c, d = combo
            template = rng.choice(THREE_STEP_TEMPLATES)
            instruction = template.format(a=a, b=b, c=c, d=d)
            scene = make_random_scene(colors)
            plan = make_plan_three(a, b, c, d)
            examples.append(format_example(instruction, scene, plan))

    # Error examples (place on itself)
    for a in colors:
        template = rng.choice(ERROR_TEMPLATES)
        instruction = template.format(a=a)
        scene = make_random_scene(colors)
        plan = make_error_plan(f"Cannot place {a} on itself.")
        examples.append(format_example(instruction, scene, plan))

    # Augmentation: paraphrase via word-level perturbations
    augmented = augment(examples, rng)
    examples.extend(augmented)

    rng.shuffle(examples)
    return examples[:target_count]

