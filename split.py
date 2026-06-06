import json
import random

input_file = "data/all.jsonl"
train_file = "data/train.jsonl"
val_file = "data/val.jsonl"

with open(input_file, "r", encoding="utf-8") as f:
    data = [json.loads(line) for line in f]

random.shuffle(data)

split_idx = int(len(data) * 0.9)

train_data = data[:split_idx]
val_data = data[split_idx:]

with open(train_file, "w", encoding="utf-8") as f:
    for item in train_data:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")

with open(val_file, "w", encoding="utf-8") as f:
    for item in val_data:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")

print("Done:", len(train_data), "train /", len(val_data), "val")