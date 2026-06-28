import json
import random
import sys

input_file = sys.argv[1] if len(sys.argv) > 1 else "data/all.jsonl"
train_file = sys.argv[2] if len(sys.argv) > 2 else "data/train.jsonl"
val_file = sys.argv[3] if len(sys.argv) > 3 else "data/val.jsonl"

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