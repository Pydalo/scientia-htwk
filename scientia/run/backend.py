import os
import pickle
import threading
import faiss
from flask import Flask, request, Response
import numpy as np
import torch
from transformers import AutoModel, AutoModelForCausalLM, AutoTokenizer, TextIteratorStreamer
from waitress import serve
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent))
import config
app = Flask(__name__)


config_path = Path(config.__file__).resolve().parent

LLM_PATH = config_path / config.LLM_PATH
EMB_PATH = config_path / config.EMB_PATH
INDEX_FILE = config_path / config.INDEX_FILE
CHUNKS_FILE = config_path / config.CHUNKS_FILE

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

faiss_index = faiss.read_index(str(INDEX_FILE))
with open(CHUNKS_FILE, "rb") as f:
    all_chunks = pickle.load(f)


def search_vector_lib(query_text, k=2):
    """Sucht die k relevantesten Abschnitte mit korrekter E5-Normalisierung."""
    inputs = emb_tokenizer(
        [f"query: {query_text}"], padding=True, truncation=True, max_length=800, return_tensors="pt"
    ).to(device)

    with torch.no_grad():
        outputs = emb_model(**inputs)

    attention_mask = inputs['attention_mask']
    token_embeddings = outputs.last_hidden_state
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1)
    sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
    query_vector = sum_embeddings / sum_mask

    query_vector = torch.nn.functional.normalize(query_vector, p=2, dim=1)
    query_vector = query_vector.cpu().numpy().astype("float32")

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
            context_text = "\n---\n".join(extra_infos)

            extended_context = config.EXTENDED_CONTEXT(context_text=context_text, user_query=user_query)

            for msg in reversed(messages):
                if msg["role"] == "user":
                    msg["content"] = extended_context
                    break

    system = {
        "role": "system",
        "content": config.SYSTEM_PROMT,
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


def start():
    print(f"Server started on port {config.PORT} via Waitress WSGI")
    serve(app, host=config.HOST, port=config.PORT, threads=config.THREADS)

if __name__ == "__main__":
    print(f"Server started on port {config.PORT} via Waitress WSGI")
    serve(app, host=config.HOST, port=config.PORT, threads=config.THREADS)