from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    Trainer,
    TrainingArguments
)
from datasets import load_dataset
import torch
import os

"""
poetos ji svenjar mi lingant ji lomea:

flodea flosos woli hapant
herisea veri sro sifte
tulpas role les wisa it posant
svenjar liso mi sifte

svirea veri hi mi sifta
andre antrophilasia boso esa mi aros:
lo fari wihesia ranhetol
svenjar bronetel mi myosa

O svenja O svenjar
wila ev ji masari masar
sos giv wos smje compe gigase
sos brone PALI JAREPAR
"""

def main():
    os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

    model_path = "../../models/Qwen2.5-0.5B-Instruct"

    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForCausalLM.from_pretrained(model_path)

    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    print(f"Training on: {device}")
    dataset = load_dataset("json", data_files={
        "train": "data/train.jsonl",
        "validation": "data/val.jsonl"
    })

    def format_chat(example):
        messages = example["messages"]

        example["text"] = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=False
        )

        return example

    dataset = dataset.map(format_chat)

    def tokenize_function(examples):
        text = examples["text"]

        enc = tokenizer(text, truncation=True, padding="max_length", max_length=512)

        labels = enc["input_ids"].copy()

        enc["labels"] = labels

        return enc

    tokenized = dataset.map(tokenize_function, batched=True)

    tokenized.set_format(
        type="torch",
        columns=["input_ids", "attention_mask", "labels"]
    )
    training_args = TrainingArguments(
        output_dir="../../models/Scientia1-0.5B",
        num_train_epochs=1,
        per_device_train_batch_size=1,
        save_steps=100,
        save_total_limit=2,
        logging_steps=10,
        learning_rate=2e-5,
        fp16=False,
        report_to=["tensorboard"],
    )
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized["train"],
        eval_dataset=tokenized["validation"],
    )

    checkpoint_dir = "../../models/Scientia1-0.5B"

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

    trainer.save_model("../../models/Scientia1-0.5B")
    tokenizer.save_pretrained("../../models/Scientia1-0.5B")

    print("Done.")


if __name__ == "__main__":
    import multiprocessing
    multiprocessing.freeze_support()
    main()