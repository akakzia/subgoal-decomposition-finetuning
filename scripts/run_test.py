from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
import torch
import json

MODEL_NAME = "Qwen/Qwen2.5-0.5B-Instruct"

bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.float16,
        bnb_4bit_use_double_quant=True,
    )

# Reload for inference
base_model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME, quantization_config=bnb_config, device_map="auto", trust_remote_code=True
)
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
model = PeftModel.from_pretrained(base_model, "./sft_output/final")
model.eval()

system_prompt = (
    'You are a robot task planner. Given a natural language instruction and the '
    'current scene state, decompose the instruction into a sequence of '
    'pick-and-place subgoals. Output ONLY a JSON array of steps. Each step has '
    'keys: "step" (int), "action" ("pick_and_place"), "pick" (color name), '
    '"place_on" (color name). If the instruction is invalid or impossible, '
    'output: [{"step": 1, "action": "error", "reason": "<explanation>"}]'
)

test_instruction = "Stack the red block on the blue block, then place green on top."
test_scene = json.dumps({"blocks": ["red", "blue", "green"], "positions": {"red": [0.1, 0.0, 0.02], "blue": [0.0, 0.1, 0.02], "green": [-0.1, 0.0, 0.02]}})
user_msg = f"Instruction: {test_instruction}\nScene: {test_scene}"

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": user_msg},
]
text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
inputs = tokenizer(text, return_tensors="pt").to(model.device)

with torch.no_grad():
    outputs = model.generate(**inputs, max_new_tokens=256, temperature=0.1, do_sample=True)

response = tokenizer.decode(outputs[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True)
print("Generated plan:")
print(response)