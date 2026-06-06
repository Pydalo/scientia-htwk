# README of Project for LLM '***Scientia***'
## 1. Overview
* Author: *Pydalo / Peter Helmut Wohlfarth*
* Date (begin): 6-6-2026
* Use: **Chatbot** for students of *HTWK Leipzig*
* Langauge: German (de)
* Operating System: Windows OS (v10 + 11)

## 2. Models:
* Test model for my home-pc (no CUDA): `Qwen3-0.6B`
    + Higgingface ID: `Qwen/Qwen3-0.6B`
    + Thinking: `true`
    + Parameter: `500 B`
    + Open LLM Leaderboard: `43 P`


* Test model for my home-pc but non thinking (no CUDA): `Qwen2.5-0.5B-Instruct`
    + Higgingface ID: `Qwen/Qwen2.5-0.5B-Instruct`
    + Thinking: `false`
    + Parameter: `500 B`
    + Open LLM Leaderboard: `38..43 P`


> Hopefully final model:
* Model for HTWK Leipzig (CUDA): `Qwen3 4B`
    + Higgingface ID: `Qwen/Qwen3 4B`
    + Thinking: `false`
    + Parameter: `400 M`
    + Open LLM Leaderboard: `12 P`

### 3 Packages:

We are use `PIP` as a library manager and run the project on a **local virtual environment**
That are all packages installed:

Package (Version)
-------------------------------
* absl-py (2.3.1)
* accelerate (1.11.0)
* aiohappyeyeballs (2.6.1)
* aiohttp (3.13.2)
* aiosignal (1.4.0)
* altgraph (0.17.5)
* anyio (4.11.0)
* async-timeout (5.0.1)
* attrs (25.4.0)
* blinker (1.9.0)
* certifi (2025.10.5)
* charset-normalizer (3.4.4)
* click (8.3.0)
* colorama (0.4.6)
* datasets (4.3.0)
* dill (0.4.0)
* exceptiongroup (1.3.0)
* filelock (3.20.0)
* Flask (3.1.3)
* frozenlist (1.8.0)
* fsspec (2025.9.0)
* grpcio (1.76.0)
* h11 (0.16.0)
* httpcore (1.0.9)
* httpx (0.28.1)
* huggingface-hub (0.36.0)
* idna (3.11)
* itsdangerous (2.2.0)
* Jinja2 (3.1.6)
* joblib (1.5.2)
* macholib (1.16.4)
* Markdown (3.9)
* MarkupSafe (3.0.3)
* modulegraph (0.19.7)
* mpmath (1.3.0)
* multidict (6.7.0)
* multiprocess (0.70.16)
* mwparserfromhell (0.7.2)
* networkx (3.4.2)
* numpy (2.2.6)
* packaging (25.0)
* pandas (2.3.3)
* pillow (12.0.0)
* pip (25.3)
* propcache (0.4.1)
* protobuf (6.33.0)
* psutil (7.1.2)
* py2app (0.28.9)
* pyarrow (22.0.0)
* python-dateutil (2.9.0.post0)
* pytz (2025.2)
* PyYAML (6.0.3)
* regex (2025.10.23)
* requests (2.32.5)
* safetensors (0.6.2)
* scikit-learn (1.7.2)
* scipy (1.15.3)
* setuptools (80.3.1)
* six (1.17.0)
* sniffio (1.3.1)
* sympy (1.14.0)
* tensorboard (2.20.0)
* tensorboard-data-server (0.7.2)
* threadpoolctl (3.6.0)
* tokenizers (0.22.1)
* torch (2.9.0)
* tqdm (4.67.1)
* transformers (4.57.1)
* typing_extensions (4.15.0)
* tzdata (2025.2)
* urllib3 (2.5.0)
* waitress (3.0.2)
* Werkzeug (3.1.3)
* xxhash (3.6.0)
* yarl (1.22.0)
