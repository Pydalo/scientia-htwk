from flask import Flask, request
from transformers import AutoTokenizer, AutoModelForCausalLM
from waitress import serve

app = Flask(__name__)


path = "../../models/Scientia1-0.5B"

tokenizer = AutoTokenizer.from_pretrained(path)
model = AutoModelForCausalLM.from_pretrained(path)

@app.post("/chat")
def chat():
    data = request.get_json()

    if not data or "messages" not in data:
        return {"error": "invalid request"}, 400

    messages = data["messages"]
    messages = [
        m for m in messages
        if isinstance(m, dict)
        and "role" in m
        and "content" in m
    ]

    system = {
        "role": "system",
        "content": "Du bist Scientia, ein KI-Tutor für Studierende der HTWK Leipzig. Antworte auf Deutsch in Markdown."
    }

    messages = [system] + messages[-12:]

    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    inputs = tokenizer(text, return_tensors="pt")

    outputs = model.generate(**inputs, max_new_tokens=300)

    answer = tokenizer.decode(
        outputs[0][inputs["input_ids"].shape[1]:],
        skip_special_tokens=True
    )

    if not isinstance(answer, str):
        answer = ""

    return {"answer": answer}

if __name__ == "__main__":
    print("Server started on port 5000 via Waitress WSGI")
    serve(app, host="127.0.0.1", port=5000, threads=4)
    print("Server stopped")