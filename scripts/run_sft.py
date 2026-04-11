import json

import torch
from datasets import Dataset
from peft import LoraConfig
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from trl import SFTConfig, SFTTrainer



DATASET_PATH = "data/subgoal_decomposition_dataset.jsonl"
MODEL_NAME = "Qwen/Qwen2.5-0.5B-Instruct"

def main():
    with open(DATASET_PATH) as f:
        raw = [json.loads(line) for line in f]

    dataset = Dataset.from_list(raw)
    split = dataset.train_test_split(test_size=0.2, seed=42)
    train_ds, eval_ds = split["train"], split["test"]
    print(f"Train: {len(train_ds)}, Eval: {len(eval_ds)}")

    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.float16,
        bnb_4bit_use_double_quant=True,
    )

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        quantization_config=bnb_config,
        device_map="auto",
        trust_remote_code=True,
    )
    print(f"Model loaded: {model.num_parameters():,} params")

    peft_config = LoraConfig(
        r=16,
        lora_alpha=32,
        lora_dropout=0.05,
        target_modules=["q_proj", "v_proj", "k_proj", "o_proj"],
        task_type="CAUSAL_LM",
    )

    training_args = SFTConfig(
        output_dir="./sft_output",
        num_train_epochs=5,
        per_device_train_batch_size=4,
        gradient_accumulation_steps=4,
        learning_rate=2e-4,
        warmup_ratio=0.1,
        lr_scheduler_type="cosine",
        logging_steps=10,
        save_strategy="epoch",
        eval_strategy="epoch",
        fp16=False,
        max_length=512,
        seed=42,
        report_to="none",  # change to "wandb" to enable logging
    )

    trainer = SFTTrainer(
        model=model,
        args=training_args,
        train_dataset=train_ds,
        eval_dataset=eval_ds,
        processing_class=tokenizer,
        peft_config=peft_config,
    )

    # trainer.train()

    trainer.save_model("./sft_output/final")
    tokenizer.save_pretrained("./sft_output/final")
    print("Model saved!")


if __name__ == "__main__":
    main()
