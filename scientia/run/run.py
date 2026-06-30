from transformers import AutoTokenizer, AutoModelForCausalLM
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent))
import config

def start():
    path = Path(Path(config.__file__).resolve().parent, config.LLM_PATH)

    tokenizer = AutoTokenizer.from_pretrained(path)
    model = AutoModelForCausalLM.from_pretrained(path)

    history = [
        {
            "role": "system",
            "content": config.SYSTEM_PROMT
        }
    ]

    while True:
        user_input = input("> ")

        if user_input == "exit" or user_input == "quit" or user_input == "q":
            break

        history.append({
            "role": "user",
            "content": user_input
        })

        text = tokenizer.apply_chat_template(
            history,
            tokenize=False,
            add_generation_prompt=True
        )

        inputs = tokenizer(text, return_tensors="pt")

        outputs = model.generate(
            **inputs,
            max_new_tokens=1000,
            do_sample=True
        )

        answer = tokenizer.decode(
            outputs[0][inputs["input_ids"].shape[1]:],
            skip_special_tokens=True
        )

        print(answer)

        history.append({
            "role": "assistant",
            "content": answer
        })
        
if __name__ == "__main__":
    start()