import json
import random
import sys

from pathlib import Path
script_path = Path(__file__).resolve().parent.absolute()

def start(input_file, ouput_dir):
    train_file = Path(ouput_dir, "train.jsonl")
    val_file = Path(ouput_dir, "val.jsonl")
    
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
    
if __name__ == "__name__":    
    start(str(script_path / "data/all.jsonl"), str(script_path / "data"))