import os
import faiss
import numpy as np
import pickle
from transformers import AutoTokenizer, AutoModel
import torch

emb_model_path = "../../../models/intfloat/multilingual-e5-small"
emb_tokenizer = AutoTokenizer.from_pretrained(emb_model_path)
emb_model = AutoModel.from_pretrained(emb_model_path).cpu()

def get_embeddings(texts):
    prefixed_texts = [f"passage: {t}" for t in texts]
    device = "cuda" if torch.cuda.is_available() else "cpu"
    inputs = emb_tokenizer(prefixed_texts, padding=True, truncation=True, max_length=512, return_tensors="pt").to(device)
    with torch.no_grad():
        outputs = emb_model(**inputs)
    embeddings = outputs.last_hidden_state.mean(dim=1).cpu().numpy()
    return embeddings.astype('float32')

markdown_ordner = "../data/veclib/md"
text_chunks = []

for datei in os.listdir(markdown_ordner):
    if datei.endswith(".md"):
        with open(os.path.join(markdown_ordner, datei), "r", encoding="utf-8") as f:
            inhalt = f.read()
            chunks = [c.strip() for c in inhalt.split("\n\n") if len(c.strip()) > 20]
            text_chunks.extend(chunks)

embeddings = get_embeddings(text_chunks)
dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

faiss.write_index(index, "../data/veclib/vektorbase.index")
with open("../data/veclib/text_chunks.pkl", "wb") as f:
    pickle.dump(text_chunks, f)

print(f"{len(text_chunks)} Successfully to save!")
