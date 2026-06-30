import os
import sys
import faiss
import numpy as np
import pickle
from transformers import AutoTokenizer, AutoModel
import torch
import pathlib

script_dir = pathlib.Path(__file__).resolve().parent
sys.path.append(str(script_dir.parent))

from run import config

emb_model_path = pathlib.Path(config.__file__).resolve().parent / config.EMB_PATH
emb_tokenizer = AutoTokenizer.from_pretrained(emb_model_path)
emb_model = AutoModel.from_pretrained(emb_model_path).cpu()

def get_embeddings(texts):
    if not texts:
        return np.empty((0, emb_model.config.hidden_size), dtype='float32')
        
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    model = emb_model.to(device)
    
    prefixed_texts = [f"passage: {t}" for t in texts]
    inputs = emb_tokenizer(prefixed_texts, padding=True, truncation=True, max_length=512, return_tensors="pt").to(device)

    with torch.no_grad():
        outputs = model(**inputs)

    attention_mask = inputs['attention_mask']
    token_embeddings = outputs.last_hidden_state
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1)
    sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
    embeddings = sum_embeddings / sum_mask

    embeddings = torch.nn.functional.normalize(embeddings, p=2, dim=1)
    return embeddings.cpu().numpy().astype('float32')

def start(src, dst):
    markdown_ordner = pathlib.Path(src)
    text_chunks = []

    if not markdown_ordner.exists():
        print(f"Fehler: Der Ordner {markdown_ordner} wurde nicht gefunden!")
        sys.exit(1)

    for datei in os.listdir(markdown_ordner):
        if datei.endswith(".md"):
            with open(os.path.join(markdown_ordner, datei), "r", encoding="utf-8") as f:
                lines = f.readlines()

                current_chunk = []
                for line in lines:
                    if line.startswith("#") and len("".join(current_chunk)) > 100:
                        text_chunks.append("".join(current_chunk).strip())
                        current_chunk = []
                    current_chunk.append(line)

                if current_chunk:
                    text_chunks.append("".join(current_chunk).strip())

    if not text_chunks:
        print(f"Fehler: Keine Text-Chunks in {markdown_ordner} gefunden. Überprüfe, ob dort gültige .md-Dateien liegen.")
        sys.exit(1)

    print(f"{len(text_chunks)} Chunks gefunden. Starte Embedding-Generierung...")
    embeddings = get_embeddings(text_chunks)
    dimension = embeddings.shape[1]

    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings)

    output_dir = pathlib.Path(dst)
    output_dir.mkdir(parents=True, exist_ok=True)

    faiss.write_index(index, str(output_dir / "vektorbase.index"))
    with open(output_dir / "text_chunks.pkl", "wb") as f:
        pickle.dump(text_chunks, f)

    print(f"Erfolgreich gespeichert in {output_dir}!")
    
if __name__ == "__main__":
    start(script_dir.parent / "data" / "veclib" / "md", script_dir.parent / "data" / "veclib")