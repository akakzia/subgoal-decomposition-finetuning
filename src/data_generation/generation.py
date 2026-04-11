import random 
from data_generation.constants import GRID_POSITIONS


def make_plan_single(a: str, b: str) -> list[dict]:
    return [{"step": 1, "action": "pick_and_place", "pick": a, "place_on": b}]


def make_plan_two(a: str, b: str, c: str) -> list[dict]:
    return [
        {"step": 1, "action": "pick_and_place", "pick": a, "place_on": b},
        {"step": 2, "action": "pick_and_place", "pick": c, "place_on": a},
    ]


def make_plan_three(a: str, b: str, c: str, d: str) -> list[dict]:
    return [
        {"step": 1, "action": "pick_and_place", "pick": a, "place_on": b},
        {"step": 2, "action": "pick_and_place", "pick": c, "place_on": a},
        {"step": 3, "action": "pick_and_place", "pick": d, "place_on": c},
    ]


def make_error_plan(reason: str) -> list[dict]:
    return [{"step": 1, "action": "error", "reason": reason}]


def make_random_scene(blocks: list[str]) -> dict:
    positions = random.sample(GRID_POSITIONS, len(blocks))
    return {
        "blocks": blocks,
        "positions": {b: p for b, p in zip(blocks, positions)},
    }