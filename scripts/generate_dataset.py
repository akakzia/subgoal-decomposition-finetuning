"""
Synthetic dataset generator for instruction → subgoal decomposition.

Produces a JSONL file where each line is a chat-formatted example:
    {"messages": [{"role": "system", ...}, {"role": "user", ...}, {"role": "assistant", ...}]}

Usage:
    uv run -m data.generate_dataset [--output data/sft_dataset.jsonl] [--n-examples 800]
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.data_generation.generate_examples import generate_examples
from src.data_generation.constants import DEFAULT_COLORS


def main():
    parser = argparse.ArgumentParser(description="Generate SFT dataset for block-stacking planner")
    parser.add_argument("--output", type=str, default="data/subgoal_decomposition_dataset.jsonl", help="Path to output file")
    parser.add_argument("--n-examples", type=int, default=800, help="Number of examples to generate")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument(
        "--colors",
        nargs="+",
        default=DEFAULT_COLORS,
        help="Block colors to use",
    )
    args = parser.parse_args()

    examples = generate_examples(
        colors=args.colors,
        target_count=args.n_examples,
        seed=args.seed,
    )

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w") as f:
        for ex in examples:
            f.write(json.dumps(ex) + "\n")

    print(f"Wrote {len(examples)} examples to {output_path}")

    n_error = sum(1 for e in examples if '"error"' in e["messages"][2]["content"])
    n_single = sum(1 for e in examples if e["messages"][2]["content"].count('"step"') == 1 and '"error"' not in e["messages"][2]["content"])
    n_multi = len(examples) - n_error - n_single
    print(f"  Single-step: {n_single}  Multi-step: {n_multi}  Error: {n_error}")


if __name__ == "__main__":
    main()
