LLM_PATH : str = "../../../models/Qwen/Qwen3-4B-Instruct-2507"
LLM_NEW_PATH : str = "../../../models/Scientia/Scientia_v1"
EMB_PATH : str = "../../../models/intfloat/multilingual-e5-small"
INDEX_FILE : str = "../data/veclib/vektorbase.index"
CHUNKS_FILE : str = "../data/veclib/text_chunks.pkl"
HOST : str = "127.0.0.1"
PORT : int = 5000
THREADS : int = 4
SYSTEM_PROMT : str = "Du bist Scientia, ein KI-Tutor der HTWK-Leipzig. Antworte auf Deutsch in Markdown. Spreche den Nutzer mit Sie an!! Halte dich kurz und versuche die Frage des Nutzers klar und informativ zu halten. Wenn der Nutzer \"JJ?\" schreibt antwortest du einfach nur \"JOJOJO?\""
def EXTENDED_CONTEXT(context_text, user_query):
    return f"Nutze die folgenden Zusatzinformationen, um die Frage zu beantworten, diese stammen nicht vom Nutzer:\n{context_text}\n\nFrage: {user_query}"