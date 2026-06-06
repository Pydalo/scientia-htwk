# README of Project for LLM '***Scientia***'
## 1. Overview
* Author: *Pydalo / Peter Helmut Wohlfarth*
* Date (begin): 6-6-2026
* Use: **Chatbot** for students of *HTWK Leipzig*

## 2. Metadata (of python project)
### 2.1 Packages:

We are use `PIP` as a library manager and run the project on a **local virtual environment***
That are all libraries installed:

* PyTorch
* NumPy
* transformers
* accelerate
* datasets

## 3. Models:
* Test model for my home-pc (no CUDA): `Qwen3-0.6B`
    + Higgingface ID: `Qwen/Qwen3-0.6B`
    + Thinking: `true`
    + Parameter: `500 B`
    + Open LLM Leaderboard: `43 P`


* Test model for my home-pc but non thinking (no CUDA): `Qwen2.5-0.5B-Instruct`
    + Higgingface ID: `Qwen/Qwen2.5-0.5B-Instruct`
    + Thinking: `false`
    + Parameter: `500 B`
    + Open LLM Leaderboard: `43 P`


> Hopefully final model:
* Model for HTWK Leipzig (CUDA): `Qwen3 4B`
    + Higgingface ID: `Qwen/Qwen3 4B`
    + Thinking: `false`
    + Parameter: `400 M`
    + Open LLM Leaderboard: `43 P`