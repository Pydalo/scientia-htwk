import torch
from flask import Flask, request, Response
from transformers import AutoTokenizer, AutoModelForCausalLM, TextIteratorStreamer
import threading
from waitress import serve

app = Flask(__name__)

path = "../../models/Qwen/Qwen3-4B-Instruct-2507"

tokenizer = AutoTokenizer.from_pretrained(path)

device = "cuda" if torch.cuda.is_available() else "cpu"

model = AutoModelForCausalLM.from_pretrained(
    path,
    torch_dtype=torch.float16 if device == "cuda" else torch.float32
).to(device)

model.eval()


@app.post("/chat")
def chat():
    data = request.get_json()

    if not data or "messages" not in data:
        return {"error": "invalid request"}, 400

    messages = [
        m for m in data["messages"]
        if isinstance(m, dict) and "role" in m and "content" in m
    ]

    system = {
        "role": "system",
        "content": "Du bist Scientia, ein KI-Tutor der HTWK-Leipzig. Antworte auf Deutsch in Markdown. Spreche den Nutzer mit (Sie) an!!"
    }

    messages = [system] + messages[-12:]

    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    inputs = tokenizer(text, return_tensors="pt").to(device)

    streamer = TextIteratorStreamer(
        tokenizer,
        skip_special_tokens=True
    )

    gen_kwargs = dict(
        **inputs,
        streamer=streamer,
        do_sample=True,
        temperature=0.6,
        top_p=0.9,
        max_new_tokens=900,
        eos_token_id=tokenizer.eos_token_id,
        pad_token_id=tokenizer.eos_token_id
    )

    thread = threading.Thread(
        target=model.generate,
        kwargs=gen_kwargs,
        daemon=True
    )
    thread.start()

    def generate():
        for text in streamer:
            if not text:
                continue

            if system.get("content") in text:
                continue

            yield text.encode("utf-8")

    return Response(generate(), mimetype="text/plain", direct_passthrough=True)


if __name__ == "__main__":
    print("Server started on port 5000 via Waitress WSGI")
    serve(app, host="127.0.0.1", port=5000, threads=4)