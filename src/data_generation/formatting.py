import json


SYSTEM_PROMPT = (
    "You are a robot task planner. Given a natural language instruction and the "
    "current scene state, decompose the instruction into a sequence of "
    "pick-and-place subgoals. Output ONLY a JSON array of steps. Each step has "
    'keys: "step" (int), "action" ("pick_and_place"), "pick" (color name), '
    '"place_on" (color name). If the instruction is invalid or impossible, '
    'output: [{"step": 1, "action": "error", "reason": "<explanation>"}]'
)


def format_example(instruction: str, scene: dict, plan: list[dict]) -> dict:
    user_content = f"Instruction: {instruction}\nScene: {json.dumps(scene)}"
    assistant_content = json.dumps(plan)
    return {
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_content},
            {"role": "assistant", "content": assistant_content},
        ]
    }