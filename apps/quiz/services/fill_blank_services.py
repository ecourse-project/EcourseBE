def split_content(content: str):
    if not content:
        return content

    list_words = content.split()
    return [{"id": i, "word": w, "hidden": False} for i, w in enumerate(list_words, start=1)]


def get_final_content(hidden_words, res_default=""):
    if hidden_words:
        return " ".join([w.get("word") if not w.get("hidden") else f"..." for w in hidden_words])
    return res_default
