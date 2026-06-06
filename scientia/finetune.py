from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    Trainer,
    TrainingArguments
)
from datasets import load_dataset
import torch
import os


def main():
    os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

    # === Modell ===
    model_path = "../../models/Qwen2.5-0.5B-Instruct"

    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForCausalLM.from_pretrained(model_path)

    # wichtig für Training
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    print(f"Training on: {device}")

    # === Dataset ===
    dataset = load_dataset("json", data_files={
        "train": "data/train.jsonl",
        "validation": "data/val.jsonl"
    })

    # === Chat Format für Qwen ===
    def format_chat(example):
        messages = example["messages"]

        example["text"] = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=False
        )

        return example

    dataset = dataset.map(format_chat)

    # === Tokenisierung ===
    def tokenize_function(examples):
        text = examples["text"]

        enc = tokenizer(text, truncation=True, padding="max_length", max_length=512)

        labels = enc["input_ids"].copy()

        # hier später Masking einbauen (wichtig!)
        enc["labels"] = labels

        return enc

    tokenized = dataset.map(tokenize_function, batched=True)

    tokenized.set_format(
        type="torch",
        columns=["input_ids", "attention_mask", "labels"]
    )

    # === Training Args ===
    training_args = TrainingArguments(
        output_dir="../../models/scientia1-0.6B",
        num_train_epochs=1,
        per_device_train_batch_size=1,
        save_steps=100,
        save_total_limit=2,
        logging_steps=10,
        learning_rate=2e-5,
        fp16=False,
        report_to=["tensorboard"],
    )

    # === Trainer ===
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized["train"],
        eval_dataset=tokenized["validation"],
    )

    checkpoint_dir = "../../models/scientia1-0.6B"

    checkpoints = [
        os.path.join(checkpoint_dir, d)
        for d in os.listdir(checkpoint_dir)
        if d.startswith("checkpoint-") and os.path.isdir(os.path.join(checkpoint_dir, d))
    ] if os.path.exists(checkpoint_dir) else []

    if checkpoints:
        latest = sorted(checkpoints, key=os.path.getmtime)[-1]
        print(f"Resuming from: {latest}")
        trainer.train(resume_from_checkpoint=latest)
    else:
        print("Starting training...")
        trainer.train()

    trainer.save_model("../../models/scientia1-0.6B")
    tokenizer.save_pretrained("../../models/scientia1-0.6B")

    print("Done.")


if __name__ == "__main__":
    import multiprocessing
    multiprocessing.freeze_support()
    main()