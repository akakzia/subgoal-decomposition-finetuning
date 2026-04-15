# Subgoal Decomposition Fine-tuning

Fine-tunes a small language model to act as a **robot task planner**: given a natural language instruction and the current scene state, the model decomposes the instruction into an ordered sequence of structured pick-and-place subgoals.

---

## Overview

The model is trained to translate block-stacking instructions like:

> *"Stack the red block on the blue block, then place green on top."*

into a structured JSON plan:

```json
[
  {"step": 1, "action": "pick_and_place", "pick": "red", "place_on": "blue"},
  {"step": 2, "action": "pick_and_place", "pick": "green", "place_on": "red"}
]
```

When an instruction is invalid (e.g. placing a block on itself), the model outputs an error step:

```json
[{"step": 1, "action": "error", "reason": "Cannot place red on itself."}]
```

---

## Repository Structure

```
.
├── data/
│   └── subgoal_decomposition_dataset.jsonl   # Generated training dataset
├── scripts/
│   ├── generate_dataset.py                   # Dataset generation entry point
│   ├── run_sft.py                            # Fine-tuning entry point
│   └── run_test.py                           # Inference/testing script
└── src/
    └── data_generation/
        ├── constants.py       # Block colors and grid positions
        ├── templates.py       # Natural language instruction templates
        ├── generation.py      # Plan construction (single/two/three-step + errors)
        ├── formatting.py      # Chat message formatting + system prompt
        ├── augmentation.py    # Word-level synonym augmentation
        └── generate_examples.py  # Full dataset generation pipeline
```

---

## Dataset

The synthetic dataset covers three instruction complexities:

| Type | Description | Example |
|---|---|---|
| **Single-step** | Place block A on block B | *"Move red on blue."* |
| **Two-step** | Build a tower of 3 blocks | *"Stack red on blue, then green on red."* |
| **Three-step** | Build a tower of 4 blocks | *"Stack red on blue, then green on red, then yellow on green."* |
| **Error** | Invalid instruction | *"Place red on red."* |

Examples are generated from all permutations of 6 colored blocks (`red`, `blue`, `green`, `yellow`, `orange`, `purple`) using diverse instruction templates. A word-level synonym augmentation pass (replacing words like *"Place" → "Put"*, *"block" → "cube"*, etc.) further diversifies the training distribution.

Each example is formatted as a chat conversation:

```jsonl
{
  "messages": [
    {"role": "system", "content": "You are a robot task planner ..."},
    {"role": "user", "content": "Instruction: ...\nScene: {\"blocks\": [...], \"positions\": {...}}"},
    {"role": "assistant", "content": "[{\"step\": 1, ...}]"}
  ]
}
```

### Generating the dataset

```bash
uv run scripts/generate_dataset.py \
    --output data/subgoal_decomposition_dataset.jsonl \
    --n-examples 800 \
    --seed 42
```

---

## Training

Fine-tuning uses **QLoRA** (4-bit NF4 quantization + LoRA adapters) on top of [`Qwen/Qwen2.5-0.5B-Instruct`](https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct) via HuggingFace TRL's `SFTTrainer`.

Key hyperparameters:

| Parameter | Value |
|---|---|
| Base model | `Qwen/Qwen2.5-0.5B-Instruct` |
| Quantization | 4-bit NF4 (bitsandbytes) |
| LoRA rank | 16 |
| LoRA alpha | 32 |
| LoRA target modules | `q_proj`, `k_proj`, `v_proj`, `o_proj` |
| Epochs | 5 |
| Learning rate | 2e-4 |
| LR scheduler | Cosine with 10% warmup |
| Batch size | 4 (× 4 gradient accumulation steps) |
| Max sequence length | 512 tokens |

### Running fine-tuning

```bash
uv run scripts/run_sft.py
```

The fine-tuned adapter is saved to `./sft_output/final/`.

To enable Weights & Biases logging, change `report_to="none"` to `report_to="wandb"` in `run_sft.py`.

---

## Inference

After training, load the LoRA adapter on top of the base model and run inference:

```bash
uv run scripts/run_test.py
```

This runs a hardcoded test scene through the model and prints the generated JSON plan.

---

## Setup

This project uses [`uv`](https://github.com/astral-sh/uv) for dependency management and requires Python 3.12+. PyTorch is pulled from the CUDA 12.8 index.

```bash
uv sync
```

### Dependencies

- `torch` 2.10 (CUDA 12.8)
- `transformers` ≥ 5.5
- `peft` ≥ 0.18
- `trl` ≥ 1.0
- `bitsandbytes` ≥ 0.49
- `datasets` ≥ 4.8
- `accelerate` ≥ 1.13
- `wandb` ≥ 0.25
