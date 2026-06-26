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
    device = "cuda" if torch.cuda.is_available() else "cpu"
    prefixed_texts = [f"passage: {t}" for t in texts]
    inputs = emb_tokenizer(prefixed_texts, padding=True, truncation=True, max_length=512, return_tensors="pt").to(
        device)

    with torch.no_grad():
        outputs = emb_model(**inputs)

    # Korrektes Mean-Pooling
    attention_mask = inputs['attention_mask']
    token_embeddings = outputs.last_hidden_state
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1)
    sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
    embeddings = sum_embeddings / sum_mask

    # L2-Normalisierung für Kosinus-Ähnlichkeit
    embeddings = torch.nn.functional.normalize(embeddings, p=2, dim=1)
    return embeddings.cpu().numpy().astype('float32')

markdown_ordner = "../data/veclib/md"
text_chunks = []

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

embeddings = get_embeddings(text_chunks)
dimension = embeddings.shape[1]

index = faiss.IndexFlatIP(dimension)
index.add(embeddings)

faiss.write_index(index, "../data/veclib/vektorbase.index")
with open("../data/veclib/text_chunks.pkl", "wb") as f:
    pickle.dump(text_chunks, f)

print(f"{len(text_chunks)} Successfully to save!")
