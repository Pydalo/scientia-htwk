import os
import pickle
import threading
import faiss
from flask import Flask, request, Response
import numpy as np
import torch
from transformers import AutoModel, AutoModelForCausalLM, AutoTokenizer, TextIteratorStreamer
from waitress import serve

app = Flask(__name__)

LLM_PATH = "../../../models/Qwen/Qwen3-4B-Instruct-2507"
EMB_PATH = "../../../models/intfloat/multilingual-e5-small"
INDEX_FILE = "../data/veclib/vektorbase.index"
CHUNKS_FILE = "../data/veclib/text_chunks.pkl"

device = "cuda" if torch.cuda.is_available() else "cpu"

tokenizer = AutoTokenizer.from_pretrained(LLM_PATH)
model = AutoModelForCausalLM.from_pretrained(
    LLM_PATH,
    torch_dtype=torch.float16 if device == "cuda" else torch.float32
).to(device)
model.eval()

print("Loading vector libraries...")
emb_tokenizer = AutoTokenizer.from_pretrained(EMB_PATH)
emb_model = AutoModel.from_pretrained(EMB_PATH).to(device)
emb_model.eval()

faiss_index = faiss.read_index(INDEX_FILE)
with open(CHUNKS_FILE, "rb") as f:
    all_chunks = pickle.load(f)


def search_vector_lib(query_text, k=2):
    """Sucht die k relevantesten Abschnitte aus der Vektorbibliothek."""
    inputs = emb_tokenizer(
        [f"query: {query_text}"], padding=True, truncation=True, max_length=512, return_tensors="pt"
    ).to(device)

    with torch.no_grad():
        outputs = emb_model(**inputs)

    query_vector = outputs.last_hidden_state.mean(dim=1).cpu().numpy().astype("float32")

    distances, indices = faiss_index.search(query_vector, k)

    results = []
    for idx in indices[0]:
        if idx != -1 and idx < len(all_chunks):
            results.append(all_chunks[idx])
    return results


@app.post("/chat")
def chat():
    data = request.get_json()

    if not data or "messages" not in data:
        return {"error": "invalid request"}, 400

    messages = [
        m for m in data["messages"] if isinstance(m, dict) and "role" in m and "content" in m
    ]


    user_query = ""
    for msg in reversed(messages):
        if msg["role"] == "user":
            user_query = msg["content"]
            break

    if user_query:
        extra_infos = search_vector_lib(user_query, k=2)

        if extra_infos:
            kontext_text = "\n---\n".join(extra_infos)

            erweiterter_content = f"Nutze die folgenden Zusatzinformationen, um die Frage zu beantworten:\n{kontext_text}\n\nFrage: {user_query}"

            for msg in reversed(messages):
                if msg["role"] == "user":
                    msg["content"] = erweiterter_content
                    break

    system = {
        "role": "system",
        "content": "Du bist Scientia, ein KI-Tutor der HTWK-Leipzig. Antworte auf Deutsch in Markdown. Spreche den Nutzer mit Sie an!! Halte dich kurz und versuche die Frage des Nutzers klar und informativ zu halten.",
    }

    messages = [system] + messages[-12:]

    text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = tokenizer(text, return_tensors="pt").to(device)

    streamer = TextIteratorStreamer(tokenizer, skip_special_tokens=True)

    gen_kwargs = dict(
        **inputs,
        streamer=streamer,
        do_sample=True,
        temperature=0.6,
        top_p=0.9,
        max_new_tokens=900,
        eos_token_id=tokenizer.eos_token_id,
        pad_token_id=tokenizer.eos_token_id,
    )

    thread = threading.Thread(target=model.generate, kwargs=gen_kwargs, daemon=True)
    thread.start()

    def generate():
        for token_text in streamer:
            if not token_text:
                continue
            if system.get("content") in token_text:
                continue
            yield token_text.encode("utf-8")

    return Response(generate(), mimetype="text/plain", direct_passthrough=True)


if __name__ == "__main__":
    print("Server started on port 5000 via Waitress WSGI")
    serve(app, host="127.0.0.1", port=5000, threads=4)
